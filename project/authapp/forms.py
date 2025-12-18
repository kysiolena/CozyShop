from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    SetPasswordForm,
)

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


class PasswordChangeForm(BootstrapFieldsMixin, SetPasswordForm):
    class Meta:
        model = UserModel
        fields = ["new_password1", "new_password2"]


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


class SignInForm(BootstrapFieldsMixin, AuthenticationForm):
    # email = forms.EmailField(
    #     max_length=254
    # )

    class Meta:
        model = UserModel
        fields = (
            "username",
            # "email",
            "password",
        )


class SignUpForm(BootstrapFieldsMixin, UserCreationForm):
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
            "password1",
            "password2",
        )
