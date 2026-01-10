from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView

from authapp.views import ProfileTabsMixin, RedirectNoAuthenticatedUserMixin
from catalog.models import Product
from subscribe.services import Subscribe


class SubscribeProductListView(
    RedirectNoAuthenticatedUserMixin, ProfileTabsMixin, ListView
):
    template_name = "authapp/profile-subscribe-product.html"
    page_name = "Subscribe Products"
    model = Product
    paginate_by = 2

    def get_queryset(self):
        # Filter the queryset to only include subscribe products where the 'user' field
        # matches the currently logged-in user.

        subscribe = Subscribe(self.request)

        # Get current User Subscribe Product IDs
        product_ids = subscribe.get_product_ids()

        return super().get_queryset().filter(id__in=product_ids)


class SubscribeProductAddView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Get Product ID
            product_id = kwargs.get("product_id")
        except ValueError:
            message = "Product ID is invalid"

            messages.error(self.request, message)

            return JsonResponse(
                {
                    "status": "error",
                    "message": message,
                },
                status=400,
            )

        if not request.user.is_authenticated:
            message = "You should be logged in to subscribe product"

            messages.warning(self.request, message)

            return JsonResponse(
                {
                    "status": "error",
                    "message": message,
                },
                status=400,
            )

        subscribe = Subscribe(self.request)

        success = subscribe.add_item(product_id)

        if success:
            message = "You successfully subscribed to product"

            response = JsonResponse(
                {
                    "status": "success",
                    "message": message,
                }
            )

            messages.success(self.request, message)

            return response
        else:
            message = "Failed subscribe product"

            messages.error(self.request, message)

            return JsonResponse(
                {
                    "status": "error",
                    "message": message,
                },
                status=400,
            )


class SubscribeProductDeleteView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Get Product ID
            product_id = kwargs.get("product_id")
        except ValueError:
            message = "Product ID is invalid"

            messages.error(self.request, message)

            return JsonResponse(
                {
                    "status": "error",
                    "message": message,
                },
                status=400,
            )

        if not request.user.is_authenticated:
            message = "You should be logged in to unsubscribe product"

            messages.warning(self.request, message)

            return JsonResponse(
                {
                    "status": "error",
                    "message": message,
                },
                status=400,
            )

        subscribe = Subscribe(self.request)

        success = subscribe.delete_item(product_id)

        if success:
            message = "You successfully unsubscribed from product"

            response = JsonResponse(
                {
                    "status": "success",
                    "message": message,
                }
            )

            messages.success(self.request, message)

            return response
        else:
            message = "Failed unsubscribe product"

            messages.error(self.request, message)

            return JsonResponse(
                {
                    "status": "error",
                    "message": message,
                },
                status=400,
            )
