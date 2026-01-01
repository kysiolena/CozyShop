import json

from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from cart.services import Cart
from shop.views import BaseContextMixin


class CartContextMixin:
    def get_context_data(self, **kwargs):
        cart = Cart(self.request)

        cart_full_info = cart.get_full_info()

        context = super().get_context_data(**kwargs)

        context["cart_items"] = cart_full_info["cart_items"]
        context["total_price"] = cart_full_info["total_price"]
        context["total_sale_price"] = cart_full_info["total_sale_price"]

        return context


class CartListView(BaseContextMixin, CartContextMixin, TemplateView):
    template_name = "cart/index.html"
    page_name = "Cart"


class CartUpdateView(View):

    def post(self, request, *args, **kwargs):
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

        cart = Cart(self.request)

        success = cart.update(data)

        if success:
            message = "Cart was successfully updated"

            response = JsonResponse(
                {
                    "status": "success",
                    "message": message,
                    "data": {"cart_len": cart.__len__()},
                }
            )

            messages.success(self.request, message)

            return response
        else:
            messages.error(self.request, "Failed to update cart")

        return JsonResponse(
            {
                "status": "error",
                "message": "Something went wrong",
            },
            status=400,
        )


class CartCleanView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(self.request)

        success = cart.clean()

        if success:
            message = "Cart was successfully cleaned"

            response = JsonResponse(
                {
                    "status": "success",
                    "message": message,
                    "data": {"cart_len": cart.__len__()},
                }
            )

            messages.success(self.request, message)

            return response
        else:
            messages.error(self.request, "Failed to clean cart")

        return JsonResponse(
            {
                "status": "error",
                "message": "Something went wrong",
            },
            status=400,
        )


class CartAddItemView(View):
    def post(self, request, *args, **kwargs):
        try:
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

            product_id = data.get("product_id")
            quantity = data.get("quantity")

            if product_id and quantity:
                cart = Cart(self.request)

                success = cart.add_item(product_id, quantity)

                if success:
                    message = "Product successfully added to cart"

                    response = JsonResponse(
                        {
                            "status": "success",
                            "message": message,
                            "data": {"cart_len": cart.__len__()},
                        }
                    )

                    messages.success(self.request, message)

                    return response
                else:
                    messages.error(self.request, "Failed to add item")
            else:
                messages.error(
                    self.request, "Parameters product_id and quantity are required"
                )
        except json.JSONDecodeError:
            messages.error(self.request, "Invalid JSON")

        return JsonResponse(
            {
                "status": "error",
                "message": "Something went wrong",
            },
            status=400,
        )


class CartDeleteItemView(View):

    def post(self, request, *args, **kwargs):
        try:
            product_id = self.kwargs.get("product_id")

            if product_id:
                cart = Cart(self.request)

                success = cart.delete_item(product_id)

                if success:
                    message = "Product was successfully deleted from cart"

                    response = JsonResponse(
                        {
                            "status": "success",
                            "message": message,
                            "data": {"cart_len": cart.__len__()},
                        }
                    )

                    messages.success(self.request, message)

                    return response
                else:
                    messages.error(self.request, "Failed to delete item")
            else:
                messages.error(self.request, "Parameter product_id is required")
        except json.JSONDecodeError:
            messages.error(self.request, "Invalid JSON")

        return JsonResponse(
            {
                "status": "error",
                "message": "Something went wrong",
            },
            status=400,
        )
