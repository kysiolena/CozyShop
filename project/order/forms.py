from django import forms

from order.models import ShippingAddress
from shop.forms import BootstrapFieldsMixin


class ShippingAddressForm(BootstrapFieldsMixin, forms.ModelForm):
    shipping_full_name = forms.CharField(label="Full Name")
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
            "shipping_address1",
            "shipping_address2",
            "shipping_city",
            "shipping_state",
            "shipping_zipcode",
            "shipping_country",
        )
        exclude = ("user",)
