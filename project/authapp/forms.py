from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    PasswordChangeForm as BasePasswordChangeForm,
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm,
)

from authapp.models import Profile
from shop.forms import BootstrapFieldsMixin

# Get User Current Model
UserModel = get_user_model()


class ProfileBillingInfoUpdateForm(BootstrapFieldsMixin, forms.ModelForm):
    address1 = forms.CharField(label="Street, building")
    address2 = forms.CharField(label="Apartment, etc.")

    class Meta:
        model = Profile
        fields = (
            "phone",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
            "country",
        )


class ProfileAvatarUpdateForm(BootstrapFieldsMixin, forms.ModelForm):

    class Meta:
        model = Profile
        fields = ("image",)


class ProfileUpdateForm(BootstrapFieldsMixin, UserChangeForm):
    # Hide password stuff
    password = None

    # Get other fields
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )

    class Meta:
        model = UserModel
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )


class PasswordResetConfirmForm(BootstrapFieldsMixin, SetPasswordForm):
    class Meta:
        model = UserModel
        fields = ["new_password1", "new_password2"]


class PasswordResetForm(BootstrapFieldsMixin, BasePasswordResetForm):
    class Meta:
        model = UserModel
        fields = ["email"]

    def clean_email(self):
        """Raise ValidationError if user doesn't exist."""
        email = self.cleaned_data.get("email")

        # Check if any active user exists with this email
        if not UserModel.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError(
                "There is no active user registered with this email address."
            )
        return email


class PasswordChangeForm(BootstrapFieldsMixin, BasePasswordChangeForm):
    class Meta:
        model = UserModel
        fields = ["new_password1", "new_password2"]


class SignInForm(BootstrapFieldsMixin, AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        label="Email",
        help_text="Enter the email address you used when registering.",
    )

    class Meta:
        model = UserModel
        fields = (
            "username",
            "password",
        )


class SignUpForm(BootstrapFieldsMixin, UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Inform a valid email address.",
        required=True,
    )

    class Meta:
        model = UserModel
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
