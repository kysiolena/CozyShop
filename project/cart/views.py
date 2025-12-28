import json

from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from cart.services import Cart
from catalog.models import Product
from shop.views import BaseContextMixin


class CartContextMixin:
    def get_context_data(self, **kwargs):
        cart = Cart(self.request)

        # Get Cart ids
        cart_ids = cart.get_ids()

        # Get Products info related to Cart items
        products = Product.objects.filter(id__in=cart_ids)

        # Total Cart
        total_price = 0
        total_sale_price = 0

        # Create full Cart items
        cart_item_full = []
        for product in products:
            item = cart.get_item(product.id)

            if item:
                # Calculate total item price
                total_item_price = product.price * item["quantity"]
                # Without sale total item price and total item sale price are equal
                total_item_sale_price = total_item_price

                if product.sale_price:
                    total_item_sale_price = product.sale_price * item["quantity"]

                # Add total item price to total cart price
                total_price += total_item_price
                # Add total item sale price to total cart sale price
                total_sale_price += total_item_sale_price

                # Combine full cart item dict
                cart_item_full.append(
                    {
                        "product": product,
                        "quantity": item["quantity"],
                        "total_price": round(total_item_price, 2),
                        "total_sale_price": round(total_item_sale_price, 2),
                    }
                )

        context = super().get_context_data(**kwargs)

        context["cart_items"] = cart_item_full
        context["total_price"] = round(total_price, 2)
        context["total_sale_price"] = round(total_sale_price, 2)

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
