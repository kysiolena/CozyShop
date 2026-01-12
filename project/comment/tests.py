from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import Product, Category
from comment.models import Comment
from order.models import Order, OrderItem, Status

User = get_user_model()


class CommentModelTest(TestCase):
    """
    Tests for the Comment database model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="commenter", email="comment@test.com", password="password"
        )
        self.category = Category.objects.create(name="Test Cat", slug="test-cat")
        self.product = Product.objects.create(
            name="Test Product", slug="test-prod", price=100.0, in_stock=True
        )
        self.product.categories.add(self.category)

    def test_create_comment(self):
        """Test creating a comment instance."""
        comment = Comment.objects.create(
            user=self.user,
            product=self.product,
            body="Great product!",
        )
        self.assertEqual(str(comment), f"Comment - {comment.id}")
        self.assertFalse(comment.is_approved)  # Should be False by default

    def test_comment_img_property(self):
        """Test the image property fallback."""
        comment = Comment.objects.create(
            user=self.user,
            product=self.product,
            body="No image here",
        )
        self.assertIsNone(comment.img)


class CommentViewTest(TestCase):
    """
    Tests for the Comment Views (access control and logic).
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="reviewer", email="review@test.com", password="password"
        )
        self.category = Category.objects.create(name="View Cat", slug="view-cat")
        self.product = Product.objects.create(
            name="View Product", slug="view-prod", price=50.0, in_stock=True
        )
        self.product.categories.add(self.category)

        self.url = reverse("comment_create_page", args=[self.product.id])

    def test_create_comment_unauthenticated(self):
        """Unauthenticated users cannot create comments."""
        # Use follow=True to get the final page context where messages are displayed
        response = self.client.post(self.url, {"body": "Test"}, follow=True)

        # Verify redirect
        self.assertRedirects(
            response, reverse("product_page", args=[self.product.slug])
        )

        # Verify error message
        messages = list(response.context["messages"])
        self.assertTrue(any("authenticated" in str(m) for m in messages))

    def test_create_comment_no_order(self):
        """Authenticated users WITHOUT a completed order cannot create comments."""
        self.client.force_login(self.user)

        # Use follow=True
        response = self.client.post(
            self.url, {"body": "I haven't bought this!"}, follow=True
        )

        # Verify redirect
        self.assertRedirects(
            response, reverse("product_page", args=[self.product.slug])
        )

        # Verify warning message
        messages = list(response.context["messages"])
        self.assertTrue(any("buy one first" in str(m) for m in messages))

    def test_create_comment_with_completed_order_success(self):
        """Users with a COMPLETED order for the product CAN create comments."""
        self.client.force_login(self.user)

        # Create a completed order for this user containing the product
        order = Order.objects.create(
            user=self.user,
            status=Status.COMPLETED,
            amount_paid=50.0,
            full_name="Reviewer",
            phone="123",
            email="review@test.com",
            shipping_address="Addr",
        )
        OrderItem.objects.create(
            order=order, product=self.product, quantity=1, price=50.0
        )

        data = {"body": "Valid review because I bought it."}
        response = self.client.post(self.url, data, follow=True)

        # Should redirect to product page on success
        self.assertRedirects(
            response, reverse("product_page", args=[self.product.slug])
        )

        # Verify comment was created
        self.assertTrue(
            Comment.objects.filter(user=self.user, product=self.product).exists()
        )
        comment = Comment.objects.get(user=self.user, product=self.product)
        self.assertEqual(comment.body, "Valid review because I bought it.")
        self.assertFalse(comment.is_approved)  # Still requires moderation

        # Verify success message
        messages = list(response.context["messages"])
        self.assertTrue(any("successfully created" in str(m) for m in messages))

    def test_create_comment_invalid_product(self):
        """Trying to comment on a non-existent product should raise error."""
        self.client.force_login(self.user)
        invalid_url = reverse("comment_create_page", args=[99999])

        # Because the view uses Product.objects.get() directly without a try/except or get_object_or_404,
        # providing an invalid ID will raise DoesNotExist.
        with self.assertRaises(Product.DoesNotExist):
            self.client.post(invalid_url)
