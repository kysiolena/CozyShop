from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

UserModel = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_staff")


admin.site.register(UserModel, CustomUserAdmin)
