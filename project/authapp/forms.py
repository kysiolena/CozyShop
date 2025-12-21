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

# Get User Current Model
UserModel = get_user_model()


class BootstrapFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop through all fields and add Bootstrap classes
        for field_name, field in self.fields.items():
            # Add form-control class to the input element
            field.widget.attrs.update({"class": "form-control"})

            # Check for checkboxes (if any) as they need a different class in Bootstrap
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})

            # Check if the form is bound and if the field has errors
            if self.is_bound and self.errors.get(field_name):
                # Get existing classes or initialize an empty list
                existing_classes = field.widget.attrs.get("class", "").split()
                # Add 'is-invalid' if it's not already there
                if "is-invalid" not in existing_classes:
                    existing_classes.append("is-invalid")
                # Update the 'class' attribute
                field.widget.attrs.update({"class": " ".join(existing_classes)})


class ProfileContactsUpdateForm(BootstrapFieldsMixin, forms.ModelForm):

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
