from django.urls import path

from authapp.views import (
    UpdatePasswordView,
    SignOutView,
    SignUpView,
    SignInView,
    ActivateAccountView,
    ResetPasswordView,
    ResetPasswordConfirmView,
    ProfileUpdateView,
    ProfileAvatarUpdateView,
    ProfileContactsUpdateView,
    ProfileDeleteView,
    ProfileDeleteConfirmView,
    ProfileBillingInfoUpdateView,
    ProfileShippingInfoUpdateView,
)

urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="sign_in_page"),
    path("sign-up/", SignUpView.as_view(), name="sign_up_page"),
    path(
        "activate/<uidb64>/<token>/",
        ActivateAccountView.as_view(),
        name="activate_page",
    ),
    path("sign-out/", SignOutView.as_view(), name="sign_out_page"),
    path("update-password/", UpdatePasswordView.as_view(), name="update_password_page"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password_page"),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm_page",
    ),
    path("profile/", ProfileUpdateView.as_view(), name="profile_page"),
    path(
        "profile/avatar/", ProfileAvatarUpdateView.as_view(), name="profile_avatar_page"
    ),
    path(
        "profile/billing-info/",
        ProfileBillingInfoUpdateView.as_view(),
        name="profile_billing_info_page",
    ),
    path(
        "profile/shipping-info/",
        ProfileShippingInfoUpdateView.as_view(),
        name="profile_shipping_info_page",
    ),
    path("profile/delete/", ProfileDeleteView.as_view(), name="profile_delete_page"),
    path(
        "profile/delete/confirm/<uidb64>/<token>/",
        ProfileDeleteConfirmView.as_view(),
        name="profile_delete_confirm_page",
    ),
]
