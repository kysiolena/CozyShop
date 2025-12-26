from django.urls import path

from order.views import (
    OrderCheckoutView,
    OrderBillingView,
    PaymentSuccessView,
    PaymentFailView,
)

urlpatterns = [
    path("checkout/", OrderCheckoutView.as_view(), name="order_checkout_page"),
    path("billing/", OrderBillingView.as_view(), name="order_billing_page"),
    path("payment/success", PaymentSuccessView.as_view(), name="payment_success_page"),
    path("payment/fail", PaymentFailView.as_view(), name="payment_fail_page"),
]
