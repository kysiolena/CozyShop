from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from authapp.models import Profile
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
    ]

    # Add image field and the new preview method to readonly_fields
    readonly_fields = ["image_preview"]


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
    ]

    # Add image field and the new preview method to readonly_fields
    readonly_fields = ["image_preview"]


# Extend User Model
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_staff")
    inlines = [ProfileInline]


admin.site.register(UserModel, CustomUserAdmin)
