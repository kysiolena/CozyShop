import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from catalog.models import Product
from order.models import (
    Order as OrderModel,
    OrderItem,
    ShippingAddress,
    Status,
    PaymentMethod,
)
from order.services import Order as OrderService

User = get_user_model()


class OrderModelTest(TestCase):
    """
    Tests for Order models and Signals.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="ordermodel", email="order@test.com", password="password"
        )

    def test_shipping_address_signal(self):
        """Test that creating a User automatically creates a ShippingAddress."""
        # Shipping address should be created by post_save signal
        self.assertTrue(ShippingAddress.objects.filter(user=self.user).exists())

    def test_order_status_info(self):
        """Test the helper method that returns status label and css class."""
        order = OrderModel.objects.create(
            amount_paid=100.00,
            full_name="Test Order",
            phone="123",
            email="test@test.com",
            status=Status.COMPLETED,
        )
        info = order.status_info()
        self.assertEqual(info["label"], "Completed")
        self.assertEqual(info["style"], "success")

        order.status = Status.PENDING
        info = order.status_info()
        self.assertEqual(info["style"], "secondary")

    def test_str_representations(self):
        """Test string representations of models."""
        order = OrderModel.objects.create(
            amount_paid=10.0, full_name="Name", phone="1", email="e@e.com"
        )
        self.assertEqual(str(order), f"Order - {order.id}")

        # Need a product for OrderItem
        product = Product.objects.create(name="P", slug="p", price=10)
        item = OrderItem.objects.create(
            order=order, product=product, price=10, quantity=1
        )
        self.assertEqual(str(item), f"Order Item - {item.id}")


class OrderServiceTest(TestCase):
    """
    Tests for the Order Service logic (services.py).
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="serviceuser", email="service@test.com", password="password"
        )

    def _get_request(self):
        request = self.factory.get("/")
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        request.user = self.user
        return request

    def test_session_storage(self):
        """Test setting and getting info from session via Service."""
        request = self._get_request()
        service = OrderService(request)

        # Shipping Info
        si_data = {"shipping_full_name": "John Doe", "shipping_city": "City"}
        service.set_si(si_data)
        self.assertEqual(service.get_si(), si_data)
        self.assertEqual(request.session[service._si_key], si_data)

        # Payment Method
        service.set_pm(PaymentMethod.PAY_PAL)
        self.assertEqual(service.get_pm(), PaymentMethod.PAY_PAL)

    @patch("order.services.Cart")
    def test_create_order_success(self, MockCart):
        """Test creating an order successfully."""
        request = self._get_request()
        service = OrderService(request)

        # 1. Setup Session Data
        service.set_pm(PaymentMethod.PAY_PAL)
        service.set_si(
            {
                "shipping_full_name": "Buyer",
                "shipping_phone": "555-0199",
                "shipping_email": "buyer@test.com",
                "shipping_address1": "123 St",
                "shipping_city": "Metropolis",
            }
        )

        # 2. Mock Cart Data
        product = Product.objects.create(name="Service Prod", slug="s-prod", price=50)

        mock_cart_instance = MockCart.return_value
        mock_cart_instance.get_full_info.return_value = {
            "total_sale_price": 100.0,
            "cart_items": [
                {"product": product, "quantity": 2, "total_sale_price": 100.0}
            ],
        }

        # 3. Create Order
        invoice = service.create()

        # 4. Assertions
        self.assertIsNotNone(invoice)
        self.assertTrue(OrderModel.objects.filter(invoice=invoice).exists())

        order = OrderModel.objects.get(invoice=invoice)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.amount_paid, 100.0)
        self.assertEqual(order.status, Status.WAIT_PAYMENT)  # PayPal default

        # Verify Items
        self.assertEqual(order.order_items.count(), 1)

        # Verify Cart cleaned
        mock_cart_instance.clean.assert_called_once()


class OrderViewTest(TestCase):
    """
    Tests for Order Views (Checkout, Billing, Creation).
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="viewuser", email="view@test.com", password="password"
        )

        # Setup Product and Cart for "EmptyCartContextRedirectMixin" checks
        # FIX 1: Ensure product is in_stock=True, otherwise Cart service hides it
        # and EmptyCartContextRedirectMixin redirects to catalog.
        self.product = Product.objects.create(
            name="View P", slug="vp", price=10, in_stock=True
        )

    def _fill_cart_session(self):
        # Manually inject cart data into session so mixin doesn't redirect
        session = self.client.session
        session["session_cart_key"] = [{"product_id": self.product.id, "quantity": 1}]
        session.save()

    def test_checkout_redirects_empty_cart(self):
        """Checkout should redirect to catalog if cart is empty."""
        url = reverse("order_checkout_page")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("catalog_page"))

    def test_checkout_view_post(self):
        """Test submitting shipping info."""
        self._fill_cart_session()
        self.client.force_login(self.user)

        url = reverse("order_checkout_page")
        data = {
            "shipping_full_name": "Test User",
            "shipping_phone": "123456789",
            "shipping_email": "test@test.com",
            "shipping_address1": "123 Street",
            # FIX 2: ShippingAddress model requires address2 (not blank=True),
            # so we must provide a non-empty value.
            "shipping_address2": "Apt 1",
            "shipping_city": "City",
            "shipping_state": "State",
            "shipping_zipcode": "00000",
            "shipping_country": "Country",
        }

        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("order_billing_page"))

        # Check session
        session = self.client.session
        self.assertIn("session_shipping_info_key", session)
        self.assertEqual(
            session["session_shipping_info_key"]["shipping_full_name"], "Test User"
        )

    def test_billing_view_redirects_no_shipping(self):
        """Billing page should redirect to checkout if shipping info is missing."""
        self._fill_cart_session()
        url = reverse("order_billing_page")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("order_checkout_page"))

    def test_billing_view_post_paypal(self):
        """Test selecting PayPal payment method."""
        self._fill_cart_session()

        # Inject shipping info so we don't get redirected
        session = self.client.session
        session["session_shipping_info_key"] = {"dummy": "data"}
        session.save()

        url = reverse("order_billing_page")
        data = {"pm": "PP"}  # PaymentMethod.PAY_PAL

        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        json_resp = json.loads(response.content)
        self.assertEqual(json_resp["status"], "success")

        # Check session
        session = self.client.session
        self.assertEqual(session["session_payment_method_key"], "PP")

    @patch("order.views.Cart")
    def test_create_order_view_success(self, MockCart):
        """Test the final order creation view."""
        # 1. Setup Session with all required data
        session = self.client.session
        session["session_cart_key"] = [{"product_id": self.product.id, "quantity": 1}]
        session["session_payment_method_key"] = "PP"
        session["session_shipping_info_key"] = {
            "shipping_full_name": "Final User",
            "shipping_phone": "111",
            "shipping_email": "f@f.com",
            "shipping_address1": "A",
            "shipping_city": "C",
        }
        session.save()

        # 2. Mock Cart behavior inside the view
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.__len__.return_value = 1
        mock_cart_instance.get_full_info.return_value = {
            "total_sale_price": 10.0,
            "cart_items": [
                {"product": self.product, "quantity": 1, "total_sale_price": 10.0}
            ],
        }
        mock_cart_instance.clean.return_value = True

        # 3. Call Create View
        url = reverse("order_create_page")
        response = self.client.get(url)

        # 4. Should redirect to self with invoice param
        self.assertEqual(response.status_code, 302)
        self.assertIn("invoice=", response.url)

        # 5. Verify DB
        self.assertTrue(OrderModel.objects.exists())
