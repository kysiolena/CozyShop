from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView


class SignInView(auth_views.LoginView):
    template_name = "authapp/sign-in.html"


class SignUpView(CreateView):
    template_name = "authapp/sign-up.html"


class SignOutView(auth_views.LogoutView):
    template_name = "authapp/sign-out.html"


class ProfileView(TemplateView):
    template_name = "authapp/profile.html"


class UpdatePasswordView(auth_views.PasswordChangeView):
    template_name = "authapp/update-password.html"
