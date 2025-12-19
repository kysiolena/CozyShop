from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

UserModel = get_user_model()


class CustomUserAdmin(UserAdmin):
    # Add email to the list of fields to display and use in forms
    list_display = ("email", "first_name", "last_name", "is_staff")
    # ... other configurations for fieldsets, etc.


admin.site.register(UserModel, CustomUserAdmin)
