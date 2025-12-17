from catalog.models import Product, Category, ProductReview
from django.contrib import admin

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductReview)
