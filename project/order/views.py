import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    DetailView,
    FormView,
)

from authapp.views import ProfileTabsMixin, RedirectNoAuthenticatedUserMixin
from cart.views import CartContextMixin
from order.forms import ShippingAddressForm, BillingInfoForm
from shop.views import BaseContextMixin


class EmptyCartContextRedirectMixin(CartContextMixin):
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


class OrderCheckoutView(BaseContextMixin, EmptyCartContextRedirectMixin, FormView):
    template_name = "order/checkout.html"
    page_name = "Checkout"
    form_class = ShippingAddressForm
    success_url = reverse_lazy("order_billing_page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["shipping_form"] = context.pop("form")

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.user.is_authenticated:
            instance = self.request.user.shipping_address

            kwargs["instance"] = instance

        return kwargs

    def get_initial(self):
        # Get the default initial data first
        initial = super().get_initial()

        shipping_info = self.request.session.get("shipping_info")

        # Update specific fields dynamically if session has shipping_info data
        if shipping_info:
            for key, value in shipping_info.items():
                initial[key] = value

        return initial

    def form_valid(self, form):
        # Save form data to session
        self.request.session["shipping_info"] = form.cleaned_data

        return super().form_valid(form)


class OrderBillingView(BaseContextMixin, EmptyCartContextRedirectMixin, TemplateView):
    template_name = "order/billing.html"
    page_name = "Billing"

    # Available payment methods
    pms_available = ["card", "paypal"]

    def get(self, request, *args, **kwargs):
        shipping_info = self.request.session.get("shipping_info")

        # Redirect to the Checkout Page if Shipping Info missed
        if not shipping_info:
            messages.warning(
                request,
                "Shipping information is missing. Please fill it out.",
            )

            return redirect("order_checkout_page")
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.body)

        try:
            # Parse the raw JSON body
            data = json.loads(request.body)
        except json.JSONDecodeError:
            message = "Invalid JSON format"

            messages.error(self.request, message)

            return JsonResponse(
                {
                    "status": "error",
                    "message": message,
                },
                status=400,
            )

        payment_method = data.get("pm")

        if payment_method in self.pms_available:
            # Save payment method in session
            self.request.session["payment_method"] = payment_method

        # Check payment method
        if payment_method == "paypal":
            return JsonResponse(
                {
                    "status": "success",
                    "message": reverse_lazy("order_create_page"),
                },
                status=200,
            )
        elif payment_method == "card":
            # Bind the billing form with the JSON data
            billing_form = BillingInfoForm(data)

            if billing_form.is_valid():
                # Service Pay by Card logic
                print("Service Pay by Card logic", data)

                # Save billing info in session
                self.request.session["billing_info"] = billing_form.cleaned_data

                return JsonResponse(
                    {
                        "status": "success",
                        "message": reverse_lazy("order_create_page"),
                    },
                    status=200,
                )
            else:
                message = "Billing form is invalid \n"

                for field_name, errors in billing_form.errors.items():
                    message += f"\n • {field_name}: {errors[0]}"

                messages.error(self.request, message)

                return JsonResponse(
                    {
                        "status": "error",
                        "message": message,
                    },
                    status=400,
                )
        else:
            message = "Payment method not available"

            messages.error(self.request, message)

            return JsonResponse(
                {
                    "status": "error",
                    "message": message,
                },
                status=400,
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        shipping_info = self.request.session.get("shipping_info")

        context["shipping_form"] = ShippingAddressForm(shipping_info or None)
        context["billing_form"] = BillingInfoForm(self.request.POST or None)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            context["billing_form"] = BillingInfoForm(
                self.request.POST or None, instance=profile
            )
        else:
            context["billing_form"] = BillingInfoForm(self.request.POST or None)

        return context


class OrderCreateView(BaseContextMixin, EmptyCartContextRedirectMixin, TemplateView):
    template_name = "order/create-process.html"
    page_name = "Order Create"
    error = None
    invoice = None

    def get(self, request, *args, **kwargs):
        shipping_info = self.request.session.get("shipping_info")
        billing_info = self.request.session.get("billing_info")
        payment_method = self.request.session.get("payment_method")

        # Redirect to the Checkout Page if Payment Method or Shipping/Billing Info missed
        if (
            not shipping_info
            or not payment_method
            or (payment_method == "card" and not billing_info)
        ):
            messages.warning(
                request,
                "Missing required parameters for creating order.",
            )

            return redirect("order_checkout_page")

        self.invoice = self.request.GET.get("invoice")

        if self.invoice:
            # Display success or failure Order Create page
            self.error = False

            return super().get(request, *args, **kwargs)
        else:
            # Create order and reload (TO DO)
            # Clean session: cart, shipping/billing address, payment_method
            self.error = False
            self.invoice = "sadsfd-safdf-fsdf"

            if self.invoice and not self.error:
                return redirect(f"{self.request.path}?invoice={self.invoice}")

        # To failed page
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.invoice:
            # Get Order
            order = {"order_id": 1}
            order_id = order.get("order_id")

            # Add form to payment to context
            pass

        context["order_id"] = order_id
        context["error"] = self.error

        return context


class PaymentCardView(View):
    pass


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
