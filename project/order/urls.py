from django.urls import path

from order.views import (
    OrderCheckoutView,
    OrderBillingView,
    OrderCreateView,
    PaymentCardView,
    PaymentSuccessView,
    PaymentFailView,
)

urlpatterns = [
    path("checkout/", OrderCheckoutView.as_view(), name="order_checkout_page"),
    path("billing/", OrderBillingView.as_view(), name="order_billing_page"),
    path("create/", OrderCreateView.as_view(), name="order_create_page"),
    path("payment/card", PaymentCardView.as_view(), name="payment_card_page"),
    path("payment/success", PaymentSuccessView.as_view(), name="payment_success_page"),
    path("payment/fail", PaymentFailView.as_view(), name="payment_fail_page"),
]
