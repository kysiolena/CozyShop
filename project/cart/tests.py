import json
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from cart.services import Cart
from catalog.models import Product, Category

User = get_user_model()


class CartServiceTest(TestCase):
    """
    Tests for the Cart service layer logic (services.py).
    """

    def setUp(self):
        # Setup basic data
        self.category = Category.objects.create(name="Cart Cat", slug="cart-cat")

        # Product 1: Standard
        self.product = Product.objects.create(
            name="Cart Product",
            slug="cart-prod",
            price=100.0,
            in_stock=True,
        )
        self.product.categories.add(self.category)

        # Product 2: On Sale
        self.product_sale = Product.objects.create(
            name="Sale Product",
            slug="sale-prod",
            price=200.0,
            sale=0.1,  # 10% off
            in_stock=True,
        )

        # Product 3: Out of Stock
        self.product_no_stock = Product.objects.create(
            name="No Stock Product",
            slug="no-stock-prod",
            price=50.0,
            in_stock=False,
        )

        self.factory = RequestFactory()

    def _get_request_with_session(self, user=None):
        """Helper to create a request with a working session."""
        request = self.factory.get("/")

        # Add session middleware manually to support request.session
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()

        if user:
            request.user = user
        else:
            # Create an anonymous user mock
            request.user = MagicMock()
            request.user.is_authenticated = False

        return request

    @patch("cart.services.send_notification_task.delay")
    def test_add_item(self, mock_task):
        """Test adding items to the cart."""
        request = self._get_request_with_session()
        cart = Cart(request)

        # Add item
        result = cart.add_item(self.product.id, 2)

        self.assertTrue(result)
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart.get_item(self.product.id)["quantity"], 2)

        # Verify notification task was called
        mock_task.assert_called_with(product_id=self.product.id)

    def test_add_duplicate_item_fails(self):
        """Test that adding an item already in cart returns False (prevent duplicates)."""
        request = self._get_request_with_session()
        cart = Cart(request)

        cart.add_item(self.product.id, 1)
        result = cart.add_item(self.product.id, 1)

        self.assertFalse(result)
        self.assertEqual(len(cart), 1)

    def test_update_cart(self):
        """Test updating the cart with new data."""
        request = self._get_request_with_session()
        cart = Cart(request)
        cart.add_item(self.product.id, 1)

        new_data = [{"product_id": self.product.id, "quantity": 5}]
        result = cart.update(new_data)

        self.assertTrue(result)
        self.assertEqual(cart.get_item(self.product.id)["quantity"], 5)

    def test_delete_item(self):
        """Test removing an item from the cart."""
        request = self._get_request_with_session()
        cart = Cart(request)
        cart.add_item(self.product.id, 1)

        result = cart.delete_item(self.product.id)

        self.assertTrue(result)
        self.assertEqual(len(cart), 0)

    def test_clean_cart(self):
        """Test emptying the entire cart."""
        request = self._get_request_with_session()
        cart = Cart(request)
        cart.add_item(self.product.id, 1)
        cart.add_item(self.product_sale.id, 1)

        result = cart.clean()

        self.assertTrue(result)
        self.assertEqual(len(cart), 0)

    def test_get_full_info_calculations(self):
        """Test total price and sale price calculations."""
        request = self._get_request_with_session()
        cart = Cart(request)

        # Add 1 normal product (100.0) and 1 sale product (200.0 - 10% = 180.0)
        cart.add_item(self.product.id, 1)
        cart.add_item(self.product_sale.id, 1)

        info = cart.get_full_info()

        # Total price (raw): 100 + 200 = 300
        self.assertEqual(info["total_price"], 300.0)

        # Total sale price: 100 + 180 = 280
        self.assertEqual(info["total_sale_price"], 280.0)

        # Check specific item details
        items = info["cart_items"]
        self.assertEqual(len(items), 2)

    def test_get_full_info_removes_out_of_stock(self):
        """Test that get_full_info automatically removes out-of-stock items."""
        request = self._get_request_with_session()
        cart = Cart(request)

        # Add out of stock item (manually force it into session since add_item doesn't check stock)
        # Note: In a real scenario, add_item might check stock, but currently services.py doesn't.
        # But get_full_info DOES check stock.
        cart._cart.append({"product_id": self.product_no_stock.id, "quantity": 1})
        request.session[cart._key] = cart._cart  # Save to session

        info = cart.get_full_info()

        # Should be empty because the item was removed
        self.assertEqual(len(info["cart_items"]), 0)
        self.assertEqual(len(cart), 0)

    def test_sync_with_profile(self):
        """Test syncing logic with a mocked authenticated user profile."""
        # Mock a user and their profile
        user = MagicMock()
        user.is_authenticated = True
        user.profile.cart_temporary = json.dumps(
            [{"product_id": self.product.id, "quantity": 3}]
        )

        request = self._get_request_with_session(user=user)
        cart = Cart(request)

        # Sync should pull data from profile to session
        cart.sync()

        self.assertEqual(len(cart), 1)
        self.assertEqual(cart.get_item(self.product.id)["quantity"], 3)

        # Verify it tries to save back to profile
        user.profile.save.assert_called()


class CartViewTest(TestCase):
    """
    Tests for the Cart Views (API endpoints).
    """

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="View Cat", slug="view-cat")
        self.product = Product.objects.create(
            name="View Product", slug="view-prod", price=50.0, in_stock=True
        )
        self.product.categories.add(self.category)

        self.list_url = reverse("cart_page")
        self.add_url = reverse("cart_add_item_page")
        self.update_url = reverse("cart_update_page")
        self.clean_url = reverse("cart_clean_page")
        self.delete_url = reverse("cart_delete_item_page", args=[self.product.id])

    @patch("cart.services.send_notification_task.delay")
    def test_add_item_view(self, mock_task):
        """Test adding an item via POST request."""
        data = {"product_id": self.product.id, "quantity": 2}

        response = self.client.post(
            self.add_url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response["status"], "success")

        # Check session
        session = self.client.session
        cart_data = session.get("session_cart_key")
        self.assertEqual(len(cart_data), 1)
        self.assertEqual(cart_data[0]["product_id"], self.product.id)

    def test_add_item_invalid_json(self):
        """Test error handling for invalid JSON."""
        response = self.client.post(
            self.add_url, "not a json", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_add_item_missing_params(self):
        """Test error handling for missing parameters."""
        data = {"product_id": self.product.id}  # Missing quantity
        response = self.client.post(
            self.add_url, json.dumps(data), content_type="application/json"
        )
        # The view catches the internal failure or logic returns error
        # Based on view logic: if not (product_id and quantity) -> messages.error
        self.assertEqual(response.status_code, 400)

    def test_update_cart_view(self):
        """Test updating cart quantity."""
        # Pre-fill session
        session = self.client.session
        session["session_cart_key"] = [{"product_id": self.product.id, "quantity": 1}]
        session.save()

        # Update to quantity 5
        data = [{"product_id": self.product.id, "quantity": 5}]
        response = self.client.post(
            self.update_url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        # Check session updated
        session = self.client.session
        self.assertEqual(session["session_cart_key"][0]["quantity"], 5)

    def test_delete_item_view(self):
        """Test deleting an item via view."""
        # Pre-fill session
        session = self.client.session
        session["session_cart_key"] = [{"product_id": self.product.id, "quantity": 1}]
        session.save()

        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 200)

        session = self.client.session
        self.assertEqual(len(session["session_cart_key"]), 0)

    def test_clean_cart_view(self):
        """Test cleaning the whole cart via view."""
        session = self.client.session
        session["session_cart_key"] = [{"product_id": self.product.id, "quantity": 1}]
        session.save()

        response = self.client.post(self.clean_url)

        self.assertEqual(response.status_code, 200)

        session = self.client.session
        self.assertEqual(len(session["session_cart_key"]), 0)

    def test_cart_list_view_context(self):
        """Test that the cart page loads with correct context."""
        session = self.client.session
        session["session_cart_key"] = [{"product_id": self.product.id, "quantity": 2}]
        session.save()

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("cart_items", response.context)
        self.assertIn("total_price", response.context)

        # Check calculated total: 50 * 2 = 100
        self.assertEqual(response.context["total_price"], 100.0)


class CartSignalTest(TestCase):
    """
    Tests for Signals (models.py).
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="signaluser", password="password", email="signal@test.com"
        )

    # Patch the Cart class specifically where it is used in cart.models
    @patch("cart.models.Cart")
    def test_user_login_syncs_cart(self, MockCart):
        """Test that logging in triggers the sync_cart signal."""

        # 1. Log the user in. Assert True to ensure login actually succeeded.
        login_success = self.client.login(email="signal@test.com", password="password")
        self.assertTrue(login_success, "Client login failed, signal won't be sent.")

        # 2. Verify Cart was initialized (which happens inside sync_cart)
        self.assertTrue(
            MockCart.called, "Cart class was not initialized inside signal handler"
        )

        # 3. Verify sync() was called on the Cart instance
        # MockCart.return_value is the 'cart' instance created in sync_cart
        MockCart.return_value.sync.assert_called_once()
