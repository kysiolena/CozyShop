from django.urls import path

from subscribe.views import SubscribeProductAddView, SubscribeProductDeleteView

urlpatterns = [
    path(
        "product/add/<int:product_id>",
        SubscribeProductAddView.as_view(),
        name="subscribe_product_add_page",
    ),
    path(
        "product/delete/<int:product_id>",
        SubscribeProductDeleteView.as_view(),
        name="subscribe_product_delete_page",
    ),
]
