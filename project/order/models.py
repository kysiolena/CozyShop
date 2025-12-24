from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Product
from shop.models import TimeStampedModel

UserModel = get_user_model()


class ShippingAddress(TimeStampedModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=200)
    shipping_address1 = models.CharField(max_length=100)
    shipping_address2 = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zipcode = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipping Address - {self.id}"


class Order(TimeStampedModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    shipping_address = models.TextField(max_length=5000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Order - {self.id}"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Order Item - {self.id}"
