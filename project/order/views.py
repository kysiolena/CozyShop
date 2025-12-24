from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from order.models import Order
from shop.views import BaseContextMixin


class OrderListView(BaseContextMixin, TemplateView):
    template_name = "order/index.html"
    page_name = "Orders' List"


class OrderCreateView(BaseContextMixin, CreateView):
    template_name = "order/create.html"
    page_name = "Create Order"
    object = Order


class OrderReadView(BaseContextMixin, DetailView):
    template_name = "order/read.html"
    page_name = "Detail Order"


class OrderUpdateView(BaseContextMixin, UpdateView):
    template_name = "order/update.html"
    page_name = "Update Order"


class OrderDeleteView(BaseContextMixin, DeleteView):
    template_name = "order/delete.html"
    page_name = "Delete Order"


class PaymentSuccessView(BaseContextMixin, TemplateView):
    template_name = "order/payment-success.html"
    page_name = "Payment Success"


class PaymentFailView(BaseContextMixin, TemplateView):
    template_name = "order/payment-fail.html"
    page_name = "Payment Fail"
