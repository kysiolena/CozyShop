from catalog.views import (
    CatalogView,
    CategoryView,
    ProductView,
    ProductReviewView,
)
from django.urls import path

urlpatterns = [
    path("", CatalogView.as_view(), name="catalog_page"),
    path("category/<str:slug>", CategoryView.as_view(), name="category_page"),
    path("product/<str:slug>", ProductView.as_view(), name="product_page"),
    path(
        "product/<str:slug>/review-create",
        ProductReviewView.as_view(),
        name="product_review_create_page",
    ),
]
