from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (
    TemplateView,
    DetailView,
)

from authapp.views import ProfileTabsMixin, RedirectNoAuthenticatedUserMixin
from cart.views import CartContextMixin
from order.forms import ShippingAddressForm, BillingInfoForm
from shop.views import BaseContextMixin


class OrderCheckoutView(BaseContextMixin, CartContextMixin, TemplateView):
    template_name = "order/checkout.html"
    page_name = "Checkout"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_items = context.get("cart_items")

        # Redirect to the Catalog Page if Cart is Empty
        if not cart_items or not len(cart_items):
            messages.warning(
                request,
                (
                    "Your cart is empty. "
                    "Before you proceed to checkout, you need to add several items to your cart."
                ),
            )

            return redirect("catalog_page")
        else:
            return super().get(request, *args, **kwargs)

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


class OrderBillingView(BaseContextMixin, CartContextMixin, TemplateView):
    template_name = "order/billing.html"
    page_name = "Billing"

    def get(self, request, *args, **kwargs):
        return redirect("order_checkout_page")

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            pass
        else:
            pass

        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["shipping_form"] = ShippingAddressForm(self.request.POST or None)

        if self.request.user.is_authenticated:

            context["billing_form"] = BillingInfoForm(
                self.request.POST or None, instance=self.request.user.profile
            )
        else:
            context["billing_form"] = BillingInfoForm(self.request.POST or None)

        return context


class PaymentSuccessView(BaseContextMixin, TemplateView):
    template_name = "order/payment-success.html"
    page_name = "Payment Success"


class PaymentFailView(BaseContextMixin, TemplateView):
    template_name = "order/payment-fail.html"
    page_name = "Payment Fail"


class OrderListView(RedirectNoAuthenticatedUserMixin, ProfileTabsMixin, TemplateView):
    template_name = "authapp/profile-orders.html"
    page_name = "Orders' List"


class OrderReadView(BaseContextMixin, DetailView):
    template_name = "authapp/profile-orders.html"
    page_name = "Orders' List"
