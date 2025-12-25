import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from authapp.forms import (
    SignUpForm,
    SignInForm,
    ProfileUpdateForm,
    PasswordChangeForm,
    PasswordResetConfirmForm,
    PasswordResetForm,
    ProfileAvatarUpdateForm,
    ProfileBillingInfoUpdateForm,
)
from order.forms import ShippingAddressForm
from shop.views import BaseContextMixin

# Logger
logger = logging.getLogger(__name__)

# Get User Current Model
UserModel = get_user_model()


class RedirectAuthenticatedUserMixin:
    """Redirects authenticated users away from 'Anonymous Only' pages."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(
                self.request,
                "You already logged in.",
            )

            # Redirect to profile page
            return redirect("profile_page")

        return super().dispatch(request, *args, **kwargs)


class RedirectNoAuthenticatedUserMixin:
    """Redirects no authenticated users away from 'Private Only' pages."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                self.request,
                f"You must be authenticated to visit the {self.page_name or ""} page.",
            )

            # Redirect to login page
            return redirect("sign_in_page")

        return super().dispatch(request, *args, **kwargs)


class SignInView(
    RedirectAuthenticatedUserMixin, BaseContextMixin, auth_views.LoginView
):
    """View for sign in with success message."""

    template_name = "authapp/sign-in.html"
    page_name = "Sign In"
    form_class = SignInForm
    next_page = "shop_page"

    def form_valid(self, form):
        """Add a success message upon successful login."""
        # The form has already authenticated the user at this point.
        # We get the user instance directly from the form.
        user = form.get_user()
        username = user.username

        messages.success(
            self.request, f"Welcome back{", " if username else ""}{username or ""}! 👋"
        )

        return super().form_valid(form)


class SignUpView(RedirectAuthenticatedUserMixin, BaseContextMixin, CreateView):
    """View for add email confirmation after successful sign up."""

    template_name = "authapp/sign-up.html"
    page_name = "Sign Up"
    form_class = SignUpForm
    success_url = reverse_lazy("shop_page")

    def form_valid(self, form):
        # 1. Save user as inactive
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Create User email confirmation
        current_site = get_current_site(self.request)
        email_subject = "Activate Your Account"

        message = render_to_string(
            template_name="authapp/emails/activate-account.html",
            context={
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            },
        )

        try:

            # 3. Send email via Mailtrap
            send_mail(
                subject=email_subject,
                message="",
                html_message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.info(
                self.request,
                "We have sent you an email, please confirm your email address to complete registration.",
            )

            return redirect(self.success_url)
        except Exception as e:
            logger.error(f"Failed to send HTML email: {e}")

            messages.error(
                self.request,
                "We are unable to send you a confirmation email, please contact our support team.",
            )

            return redirect("shop_page")


class ActivateAccountView(RedirectAuthenticatedUserMixin, View):
    """View for check User activation token and complete registration."""

    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(
                request, "Your email has been confirmed! You can now log in."
            )

            return redirect("sign_in_page")
        else:
            messages.error(request, "Activation link is invalid or has expired.")

            return redirect("shop_page")


class SignOutView(RedirectNoAuthenticatedUserMixin, auth_views.LogoutView):
    """View for log user out with displaying information message."""

    next_page = "sign_in_page"

    def get_success_url(self):
        next_page = super().get_success_url()

        messages.success(self.request, "You have been successfully logged out!")

        if next_page:
            # If next_page is defined, add the message before redirecting
            return next_page

        # If no next_page is defined, redirect to a default page (e.g., home)
        # and display the message.
        return reverse_lazy("shop_page")


class UpdatePasswordView(
    RedirectNoAuthenticatedUserMixin,
    BaseContextMixin,
    SuccessMessageMixin,
    auth_views.PasswordChangeView,
):
    """View for password change."""

    template_name = "authapp/update-password.html"
    page_name = "Update Password"
    success_url = reverse_lazy("profile_page")
    success_message = "Your password was changed successfully!"
    form_class = PasswordChangeForm


class ResetPasswordView(
    RedirectAuthenticatedUserMixin, BaseContextMixin, auth_views.PasswordResetView
):
    """View for password reset."""

    page_name = "Reset Password"
    template_name = "authapp/reset-password.html"
    success_url = reverse_lazy("shop_page")
    form_class = PasswordResetForm
    email_template_name = "authapp/emails/reset-password.html"
    html_email_template_name = "authapp/emails/reset-password.html"

    def form_valid(self, form):
        """Add success message before redirecting to shop page."""
        messages.info(
            self.request,
            "Check your email. We've sent you a password reset link. You'll find it in your inbox.",
        )

        return super().form_valid(form)


class ResetPasswordConfirmView(
    RedirectAuthenticatedUserMixin,
    BaseContextMixin,
    auth_views.PasswordResetConfirmView,
):
    """View where the user enters a new password with a success message."""

    template_name = "authapp/reset-password-confirm.html"
    page_name = "Set New Password"
    success_url = reverse_lazy("sign_in_page")
    form_class = PasswordResetConfirmForm

    def form_valid(self, form):
        """Add success message before redirecting to sign in."""
        messages.success(
            self.request,
            "Your password has been set! You may now log in with your new credentials.",
        )

        return super().form_valid(form)


class ProfileTabsMixin(BaseContextMixin):

    def get_context_data(self, **kwargs):
        tabs = [
            {"name": "Main", "url": "profile_page"},
            {"name": "Avatar", "url": "profile_avatar_page"},
            {"name": "Billing Info", "url": "profile_billing_info_page"},
            {"name": "Shipping Info", "url": "profile_shipping_info_page"},
            {"name": "Orders", "url": "profile_orders_page"},
            {"name": "Delete", "url": "profile_delete_page"},
        ]

        context = super().get_context_data(**kwargs)

        context["tabs"] = tabs

        return context


class ProfileUpdateView(
    RedirectNoAuthenticatedUserMixin, ProfileTabsMixin, SuccessMessageMixin, UpdateView
):
    """View for update main user profile information."""

    template_name = "authapp/profile.html"
    page_name = "Main Profile"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("profile_page")
    success_message = "Your profile information has been updated successfully!"

    def get_object(self, queryset=None):
        """
        Returns the object currently logged-in user.
        """

        return self.request.user


class ProfileAvatarUpdateView(
    RedirectNoAuthenticatedUserMixin, ProfileTabsMixin, SuccessMessageMixin, UpdateView
):
    """View for update user profile avatar."""

    template_name = "authapp/profile-avatar.html"
    page_name = "Avatar Profile"
    form_class = ProfileAvatarUpdateForm
    success_url = reverse_lazy("profile_avatar_page")
    success_message = "Your profile picture has been updated successfully!"

    def get_object(self, queryset=None):
        """Return the Profile instance associated with the current user."""
        return self.request.user.profile


class ProfileBillingInfoUpdateView(
    RedirectNoAuthenticatedUserMixin, ProfileTabsMixin, SuccessMessageMixin, UpdateView
):
    """View for update profile Billing Info."""

    template_name = "authapp/profile-billing-info.html"
    page_name = "Billing Info Profile"
    form_class = ProfileBillingInfoUpdateForm
    success_url = reverse_lazy("profile_billing_info_page")
    success_message = "Your profile billing info has been updated successfully!"

    def get_object(self, queryset=None):
        """Return the Profile instance associated with the current user."""
        return self.request.user.profile


class ProfileShippingInfoUpdateView(
    RedirectNoAuthenticatedUserMixin, ProfileTabsMixin, SuccessMessageMixin, UpdateView
):
    """View for update profile Shipping Info."""

    template_name = "authapp/profile-shipping-info.html"
    page_name = "Shipping Info Profile"
    form_class = ShippingAddressForm
    success_url = reverse_lazy("profile_shipping_info_page")
    success_message = "Your profile shipping info has been updated successfully!"

    def get_object(self, queryset=None):
        """Return the Shipping Address instance associated with the current user."""
        return self.request.user.shipping_address


class ProfileDeleteView(
    RedirectNoAuthenticatedUserMixin, ProfileTabsMixin, TemplateView
):
    """View for delete user profile."""

    template_name = "authapp/profile-delete.html"
    page_name = "Delete Profile"

    def post(self, request, *args, **kwargs):
        user = request.user

        # Create User email confirmation for Delete account
        current_site = get_current_site(self.request)
        email_subject = "Delete Your Account"

        message = render_to_string(
            template_name="authapp/emails/delete-account.html",
            context={
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            },
        )

        try:
            send_mail(
                subject=email_subject,
                message="",
                html_message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.info(
                self.request,
                "We have sent you an email with link to complete deletion of your account.",
            )

        except Exception as e:
            logger.error(f"Failed to send HTML email: {e}")

            messages.error(
                self.request,
                "We are unable to send you a confirmation email for delete your account, please contact our support team.",
            )

        return redirect("profile_delete_page")


class ProfileDeleteConfirmView(View):
    """View for confirming and performing user account deletion via email link."""

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            # Decode the user ID from the URL
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        # Check if the token is valid for this specific user
        if user is not None and default_token_generator.check_token(user, token):
            # Log the user out before deleting to clear the session
            logout(request)

            # Delete the user account
            user.delete()

            messages.success(
                request,
                "Your account has been permanently deleted. We're sorry to see you go.",
            )

            return redirect("shop_page")
        else:
            # If the link is tampered with or expired
            messages.error(request, "The deletion link is invalid or has expired.")

            return redirect("shop_page")
