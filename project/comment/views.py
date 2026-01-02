from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from catalog.models import Product
from comment.forms import CommentCreateForm
from order.models import Order as OrderModel, Status
from shop.views import BaseContextMixin


class CommentCreateView(BaseContextMixin, CreateView):
    template_name = "comment/create.html"
    form_class = CommentCreateForm

    def dispatch(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")

        product = Product.objects.get(id=product_id)

        self.page_name = "Create Comment"

        # Check Product exists
        if not product:
            messages.error(
                self.request,
                f"You cannot create a comment for a product that doesn't exist.",
            )

            # Redirect to Shop page
            return redirect("shop_page")
        else:
            # Check user authentication
            if not self.request.user.is_authenticated:
                messages.error(
                    self.request, "Comments can only be made by an authenticated user."
                )

                # Redirect back to Product page
                return redirect("product_page", slug=product.slug)

            # Check if User has Orders with this Product
            orders_count = (
                OrderModel.objects.filter(
                    user=self.request.user,
                    status=Status.COMPLETED,
                    order_items__product=product,
                )
                .distinct()
                .count()
            )

            if not orders_count:
                messages.warning(
                    self.request,
                    f"You didn't have any completed orders with this product. You should buy one first before creating a comment.",
                )

                # Redirect back to Product page
                return redirect("product_page", slug=product.slug)

            self.page_name += f" for «{product.name}»"

            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        product_id = self.kwargs.get("product_id")

        product_slug = Product.objects.get(id=product_id).slug

        self.success_url = reverse_lazy("product_page", kwargs={"slug": product_slug})

        messages.success(
            self.request,
            "Your comment has been successfully created and will be displayed on the product page after moderation.",
        )

        return super().get_success_url()

    def form_valid(self, form):
        # Get User ID
        user_id = self.request.user.id

        # Get Product ID
        product_id = self.kwargs.get("product_id")

        self.object = form.save(commit=False)
        self.object.user_id = user_id
        self.object.product_id = product_id
        self.object.save()

        return super().form_valid(form)
