from django.urls import path

from .views import catalog_page, product_page

urlpatterns = [
    path('', catalog_page),
    path('product/', product_page),
]
