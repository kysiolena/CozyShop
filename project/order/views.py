import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    FormView,
    ListView,
)

from authapp.views import ProfileTabsMixin, RedirectNoAuthenticatedUserMixin
from cart.services import Cart
from cart.views import CartContextMixin
from order.forms import ShippingAddressForm, BillingInfoForm
from order.models import Order as OrderModel, PaymentMethod
from order.services import Order
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

        order = Order(self.request)

        # Get Shipping Info
        shipping_info = order.get_si()

        # Update specific fields dynamically if session has shipping_info data
        if shipping_info:
            for key, value in shipping_info.items():
                initial[key] = value

        return initial

    def form_valid(self, form):
        order = Order(self.request)

        # Save form data to session
        order.set_si(form.cleaned_data)

        return super().form_valid(form)


class OrderBillingView(BaseContextMixin, EmptyCartContextRedirectMixin, TemplateView):
    template_name = "order/billing.html"
    page_name = "Billing"

    def get(self, request, *args, **kwargs):
        order = Order(self.request)

        # Get Shipping Info
        shipping_info = order.get_si()

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
        order = Order(self.request)

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

        # Save payment method in session
        is_correct_pm = order.set_pm(payment_method)

        if is_correct_pm:
            # Check payment method
            if payment_method == PaymentMethod.CARD:
                # Bind the billing form with the JSON data
                billing_form = BillingInfoForm(data)

                if billing_form.is_valid():
                    # Save billing info in session
                    order.set_bi(billing_form.cleaned_data)

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
                return JsonResponse(
                    {
                        "status": "success",
                        "message": reverse_lazy("order_create_page"),
                    },
                    status=200,
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

        order = Order(self.request)

        # Get Shipping Info
        shipping_info = order.get_si()

        # Get Billing Info
        billing_info = order.get_bi()

        context["shipping_form"] = ShippingAddressForm(shipping_info or None)
        context["billing_form"] = BillingInfoForm(billing_info or None)
        context["pyment_methods"] = PaymentMethod

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            context["billing_form"] = BillingInfoForm(
                billing_info or None, instance=profile
            )

        return context


class OrderCreateView(BaseContextMixin, TemplateView):
    template_name = "order/create-process.html"
    page_name = "Order Create"
    error = None
    invoice = None

    def get(self, request, *args, **kwargs):
        # Get invoice (if it already exists)
        self.invoice = self.request.GET.get("invoice")

        if self.invoice:
            # Display success Order Create page
            self.error = False

            return super().get(request, *args, **kwargs)
        else:
            cart = Cart(self.request)
            order = Order(self.request)

            # Get Payment Method and Shipping/Billing Info from Session
            payment_method = order.get_pm()
            shipping_info = order.get_si()
            billing_info = order.get_bi()

            # Redirect to the Checkout Page if:
            # - Payment Method missed or
            # - Shipping/Billing Info missed or
            # - Cart is empty
            if (
                not shipping_info
                or not payment_method
                or not cart.__len__()
                or (payment_method == "card" and not billing_info)
            ):
                messages.warning(
                    request,
                    "Missing required parameters for creating order.",
                )

                return redirect("order_checkout_page")

            # Create order and reload
            self.invoice = order.create()

            if self.invoice:
                return redirect(f"{self.request.path}?invoice={self.invoice}")

        self.error = True

        # Display fail Order Create page
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.invoice:
            # Get Order Service
            order = Order(self.request)

            # Get Order Model
            order_m = OrderModel.objects.get(invoice=self.invoice)

            if order_m:
                context["order_id"] = order_m.id

                if order_m.payment_method == PaymentMethod.PAY_PAL:
                    # Create PayPal form
                    paypal_form = order.create_paypal_form(order_m)

                    if paypal_form:
                        context["paypal_form"] = paypal_form

                elif order_m.payment_method == PaymentMethod.CARD:
                    # TO DO: Some logic for pay by card (maybe unnecessary)
                    pass

        context["error"] = self.error

        return context


class PaymentSuccessView(BaseContextMixin, TemplateView):
    template_name = "order/payment-success.html"
    page_name = "Payment Success"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        invoice = kwargs.get("invoice")

        if invoice:
            # Get Order Model by Invoice
            order_m = OrderModel.objects.get(invoice=invoice)

            if order_m:
                # Add Order ID to context
                context["order_id"] = order_m.id

                # Add payment_method context
                context["payment_method"] = order_m.payment_method

        return context


class PaymentFailedView(BaseContextMixin, TemplateView):
    template_name = "order/payment-failed.html"
    page_name = "Payment Failed"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        invoice = kwargs.get("invoice")

        if invoice:
            # Get Order Model by Invoice
            order_m = OrderModel.objects.get(invoice=invoice)

            if order_m:
                # Add Order ID to context
                context["order_id"] = order_m.id

                if order_m.payment_method == PaymentMethod.PAY_PAL:
                    order = Order(self.request)

                    # Create PayPal form
                    paypal_form = order.create_paypal_form(order_m)

                    if paypal_form:
                        context["paypal_form"] = paypal_form

                elif order_m.payment_method == PaymentMethod.CARD:
                    # TO DO: Some logic for pay by card (maybe unnecessary)
                    pass

        return context


class OrderListView(RedirectNoAuthenticatedUserMixin, ProfileTabsMixin, ListView):
    template_name = "authapp/profile-orders.html"
    page_name = "Orders' List"
    model = OrderModel
    paginate_by = 3

    def get_queryset(self):
        # Filter the queryset to only include orders where the 'user' field
        # matches the currently logged-in user.
        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .prefetch_related("order_items")
            .order_by("-created_at")
        )
