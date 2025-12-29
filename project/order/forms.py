from django import forms

from authapp.models import Profile
from order.models import ShippingAddress
from shop.forms import BootstrapFieldsMixin


class ShippingAddressForm(BootstrapFieldsMixin, forms.ModelForm):
    shipping_full_name = forms.CharField(label="Full Name")
    shipping_phone = forms.CharField(label="Phone")
    shipping_email = forms.EmailField(label="Email")
    shipping_address1 = forms.CharField(label="Street, building")
    shipping_address2 = forms.CharField(label="Apartment, etc.")
    shipping_city = forms.CharField(label="City")
    shipping_state = forms.CharField(label="State")
    shipping_zipcode = forms.CharField(label="Zipcode")
    shipping_country = forms.CharField(label="Country")

    class Meta:
        model = ShippingAddress
        fields = (
            "shipping_full_name",
            "shipping_phone",
            "shipping_email",
            "shipping_address1",
            "shipping_address2",
            "shipping_city",
            "shipping_state",
            "shipping_zipcode",
            "shipping_country",
        )
        exclude = ("user",)


class BillingInfoForm(BootstrapFieldsMixin, forms.ModelForm):
    card_name = forms.CharField(label="Card Name")
    card_number = forms.CharField(label="Card Number")
    card_exp_date = forms.CharField(label="Card Expiring Date")
    card_cvv_number = forms.CharField(label="Card CVV Number")
    address1 = forms.CharField(label="Street, building")
    address2 = forms.CharField(label="Apartment, etc.")
    city = forms.CharField(label="City")
    state = forms.CharField(label="State")
    zipcode = forms.CharField(label="Zipcode")
    country = forms.CharField(label="Country")

    class Meta:
        model = Profile
        fields = (
            "card_name",
            "card_number",
            "card_exp_date",
            "card_cvv_number",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
            "country",
        )
        exclude = (
            "user",
            "avatar",
        )

    def save(self, commit=True):
        billing_info = super().save(commit=False)

        print("Billing Form Save")
        for field in billing_info:
            print(field)
