from django.urls import path

from authapp.views import (
    UpdatePasswordView,
    ProfileUpdateView,
    SignOutView,
    SignUpView,
    SignInView,
)

urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="sign_in_page"),
    path("sign-up/", SignUpView.as_view(), name="sign_up_page"),
    path("sign-out/", SignOutView.as_view(), name="sign_out_page"),
    path("profile/", ProfileUpdateView.as_view(), name="profile_page"),
    path("update-password/", UpdatePasswordView.as_view(), name="update_password_page"),
]
