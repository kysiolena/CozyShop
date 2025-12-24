from django.urls import path

from order.views import (
    OrderListView,
    OrderCreateView,
    OrderReadView,
    OrderUpdateView,
    OrderDeleteView,
    PaymentSuccessView,
    PaymentFailView,
)

urlpatterns = [
    path("", OrderListView.as_view(), name="order_page"),
    path("create/", OrderCreateView.as_view(), name="order_create_page"),
    path("read/<int:order_id>", OrderReadView.as_view(), name="order_read_page"),
    path("update/<int:order_id>", OrderUpdateView.as_view(), name="order_update_page"),
    path("delete/<int:order_id>", OrderDeleteView.as_view(), name="order_delete_page"),
    path("payment/success", PaymentSuccessView.as_view(), name="payment_success_page"),
    path("payment/fail", PaymentFailView.as_view(), name="payment_fail_page"),
]
