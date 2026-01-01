from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from authapp.models import Profile
from order.models import ShippingAddress
from shop.admin import ImagePreviewMixin

UserModel = get_user_model()


class ProfileAdmin(ImagePreviewMixin, admin.ModelAdmin):
    fields = [
        "image_preview",
        "image",
        "phone",
        "address1",
        "address2",
        "city",
        "state",
        "zipcode",
        "country",
        "cart_temporary",
    ]

    # Add image field and the new preview method to readonly_fields
    readonly_fields = ["image_preview", "cart_temporary"]


admin.site.register(Profile, ProfileAdmin)


# Mix Profile and User info
class ProfileInline(ImagePreviewMixin, admin.StackedInline):
    model = Profile
    can_delete = False

    fields = [
        "image_preview",
        "image",
        "phone",
        "address1",
        "address2",
        "city",
        "state",
        "zipcode",
        "country",
        "cart_temporary",
    ]

    # Add image field and the new preview method to readonly_fields
    readonly_fields = ["image_preview", "cart_temporary"]


# Mix Shipping Address and User info
class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    can_delete = False

    fields = [
        "shipping_full_name",
        "shipping_address1",
        "shipping_address2",
        "shipping_city",
        "shipping_state",
        "shipping_zipcode",
        "shipping_country",
    ]


# Extend User Model
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_staff")
    inlines = [ProfileInline, ShippingAddressInline]


admin.site.register(UserModel, CustomUserAdmin)
