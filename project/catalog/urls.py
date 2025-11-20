from django.urls import path

from .views import CatalogView, ProductView, CategoryView

urlpatterns = [
    path("", CatalogView.as_view(), name="catalog_page"),
    path("category/<str:slug>", CategoryView.as_view(), name="category_page"),
    path("product/<str:slug>", ProductView.as_view(), name="product_page"),
]
