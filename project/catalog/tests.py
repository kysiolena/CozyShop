from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import Category, Product
from catalog.templatetags.catalog.filters import sale_price


class CatalogModelTest(TestCase):
    """
    Tests for Catalog models (Category, Product).
    """

    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-cat", description="Test Description"
        )
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-prod",
            price=100.0,
            sale=0.1,  # 10% sale
            in_stock=True,
            description="Product Description",
        )
        self.product.categories.add(self.category)

    def test_category_str(self):
        """Test Category string representation."""
        self.assertEqual(str(self.category), "Test Category")

    def test_product_str(self):
        """Test Product string representation."""
        self.assertEqual(str(self.product), "Test Product")

    def test_product_sale_price_property(self):
        """Test the model property that calculates price with discount."""
        # 100 - (100 * 0.1) = 90
        self.assertEqual(self.product.sale_price, 90.0)

    def test_product_sale_price_no_stock(self):
        """Test that sale_price returns None if product is not in stock (based on your model logic)."""
        self.product.in_stock = False
        self.product.save()
        self.assertIsNone(self.product.sale_price)

    def test_product_img_property_fallback(self):
        """Test that .img property returns default image path if no image is uploaded."""
        # We didn't upload an image in setUp
        self.assertIn("image-not-found.png", self.product.img)


class CatalogViewTest(TestCase):
    """
    Tests for the Catalog Views (views.py).
    """

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="View Cat", slug="view-cat")
        self.product = Product.objects.create(
            name="View Product", slug="view-prod", price=50.0, in_stock=True
        )
        self.product.categories.add(self.category)

    def test_catalog_page_view(self):
        """Test that the main catalog page loads and shows products."""
        url = reverse("catalog_page")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/index.html")
        self.assertIn(self.product, response.context["object_list"])
        self.assertIn(self.category, response.context["categories"])

    def test_category_page_view(self):
        """Test that the category page loads and filters products."""
        url = reverse("category_page", args=[self.category.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/category.html")

        # Check context
        self.assertEqual(response.context["category"], self.category)
        self.assertIn(self.product, response.context["object_list"])

    def test_product_page_view(self):
        """Test that the product detail page loads."""
        url = reverse("product_page", args=[self.product.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/product.html")
        self.assertEqual(response.context["object"], self.product)

    def test_search_view(self):
        """Test that the search page filters products by name."""
        # Create a product that SHOULDN'T match
        Product.objects.create(name="Hidden Item", slug="hidden", price=10)

        url = reverse("search_page")
        response = self.client.get(url, {"search": "View"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/search.html")

        products = response.context["object_list"]
        self.assertIn(self.product, products)
        self.assertEqual(len(products), 1)  # "Hidden Item" should not be here

    def test_search_view_empty_query(self):
        """Test search with empty query returns all products (or handles gracefully)."""
        url = reverse("search_page")
        response = self.client.get(url, {"search": ""})

        self.assertEqual(response.status_code, 200)
        # Should return all products if search is empty/default logic applies
        self.assertEqual(len(response.context["object_list"]), 1)


class CatalogFilterTest(TestCase):
    """
    Tests for custom template filters (templatetags/catalog/filters.py).
    """

    def test_sale_price_filter(self):
        """Test the sale_price filter logic."""
        price = 100
        sale_percent = 0.2  # 20%

        # Expected: 100 - (100 * 0.2) = 80
        result = sale_price(price, sale_percent)
        self.assertEqual(result, 80.0)

    def test_sale_price_filter_no_sale(self):
        """Test filter returns original price if sale is 0 or None."""
        self.assertEqual(sale_price(100, 0), 100)
        self.assertEqual(sale_price(100, None), 100)
