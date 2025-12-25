from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from cart.views import CartContextMixin
from order.forms import ShippingAddressForm
from order.models import Order
from shop.views import BaseContextMixin


class OrderListView(BaseContextMixin, TemplateView):
    template_name = "order/index.html"
    page_name = "Orders' List"


class OrderCheckoutView(BaseContextMixin, CartContextMixin, TemplateView):
    template_name = "order/checkout.html"
    page_name = "Checkout"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            shipping_address = self.request.user.shipping_address

            context["shipping_form"] = ShippingAddressForm(
                self.request.POST or None, instance=shipping_address
            )
        else:
            context["shipping_form"] = ShippingAddressForm(self.request.POST or None)

        return context


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
