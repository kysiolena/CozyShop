from django.urls import path, include

from order.views import (
    OrderCheckoutView,
    OrderBillingView,
    OrderCreateView,
    PaymentSuccessView,
    PaymentFailedView,
)

urlpatterns = [
    path("checkout/", OrderCheckoutView.as_view(), name="order_checkout_page"),
    path("billing/", OrderBillingView.as_view(), name="order_billing_page"),
    path("create/", OrderCreateView.as_view(), name="order_create_page"),
    path("payment/success/", PaymentSuccessView.as_view(), name="payment_success_page"),
    path("payment/failed/", PaymentFailedView.as_view(), name="payment_failed_page"),
    path("paypal/", include("paypal.standard.ipn.urls")),
]
