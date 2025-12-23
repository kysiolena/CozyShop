from django.urls import path

from cart.views import (
    CartListView,
    CartCleanView,
    CartAddItemView,
    CartDeleteItemView,
    CartUpdateView,
)

urlpatterns = [
    path("", CartListView.as_view(), name="cart_page"),
    path("update/", CartUpdateView.as_view(), name="cart_update_page"),
    path("clean/", CartCleanView.as_view(), name="cart_clean_page"),
    path("add/", CartAddItemView.as_view(), name="cart_add_item_page"),
    path(
        "delete/<int:product_id>",
        CartDeleteItemView.as_view(),
        name="cart_delete_item_page",
    ),
]
