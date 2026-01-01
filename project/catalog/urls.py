from django.urls import path

from catalog.views import (
    CatalogView,
    CategoryView,
    ProductView,
)

urlpatterns = [
    path("", CatalogView.as_view(), name="catalog_page"),
    path("category/<slug:slug>", CategoryView.as_view(), name="category_page"),
    path("product/<slug:slug>", ProductView.as_view(), name="product_page"),
]
