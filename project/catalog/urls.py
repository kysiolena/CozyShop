from django.urls import path

from .views import catalog_page, product_page, category_page

urlpatterns = [
    path("", catalog_page),
    path("category/<str:slug>", category_page, name="category_page"),
    path("product/<str:slug>", product_page, name="product_page"),
]
