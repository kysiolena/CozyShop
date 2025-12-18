from django.contrib import messages
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from authapp.forms import SignUpForm, SignInForm, ProfileUpdateForm, PasswordChangeForm
from shop.views import BaseContextMixin

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
    template_name = "authapp/sign-in.html"
    page_name = "Sign In"
    form_class = SignInForm
    next_page = "profile_page"


class SignUpView(RedirectAuthenticatedUserMixin, BaseContextMixin, CreateView):
    template_name = "authapp/sign-up.html"
    page_name = "Sign Up"
    form_class = SignUpForm
    success_url = reverse_lazy("profile_page")


class SignOutView(RedirectNoAuthenticatedUserMixin, auth_views.LogoutView):
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
    SuccessMessageMixin,
    RedirectNoAuthenticatedUserMixin,
    BaseContextMixin,
    auth_views.PasswordChangeView,
):
    template_name = "authapp/update-password.html"
    page_name = "Update Password"
    success_url = reverse_lazy("profile_page")
    success_message = "Your password was changed successfully!"
    form_class = PasswordChangeForm


class ProfileUpdateView(RedirectNoAuthenticatedUserMixin, BaseContextMixin, UpdateView):
    template_name = "authapp/profile.html"
    page_name = "Profile"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("profile_page")

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        In this case, the Profile related to the currently logged-in user. (To Do)
        """

        # Ensure the user is logged in to access their own profile
        return self.request.user
