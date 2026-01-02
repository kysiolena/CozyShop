from django.contrib import admin

from catalog.models import Product, Category
from shop.admin import ImagePreviewMixin


class CategoryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    fields = [
        "name",
        "slug",
        "description",
        "image_preview",
        "image",
    ]

    # Add image field and the new preview method to readonly_fields
    readonly_fields = ["image_preview", "created_at", "updated_at"]


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(ImagePreviewMixin, admin.ModelAdmin):
    fields = [
        "name",
        "slug",
        "description",
        "price",
        "sale",
        "in_stock",
        "categories",
        "image_preview",
        "image",
    ]

    # Add image field and the new preview method to readonly_fields
    readonly_fields = ["image_preview", "created_at", "updated_at"]


admin.site.register(Product, ProductAdmin)
