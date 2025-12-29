import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

from catalog.models import Product
from shop.models import TimeStampedModel

UserModel = get_user_model()


class ShippingAddress(TimeStampedModel):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shipping_address",
    )
    shipping_full_name = models.CharField(max_length=200)
    shipping_phone = models.CharField(max_length=20)
    shipping_email = models.EmailField(max_length=200)
    shipping_address1 = models.CharField(max_length=100)
    shipping_address2 = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zipcode = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipping Address - {self.id}"


# Create a user ShippingAddress by default when user signs up
def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        user_shipping_address = ShippingAddress(user=instance)
        user_shipping_address.save()


# Automate the shipping address thing
post_save.connect(create_shipping_address, sender=UserModel)


class Status(models.TextChoices):
    PENDING = "PE", "Pending"
    IN_PROGRESS = "IP", "In Progress"
    WAIT_PAYMENT = "WP", "Wait Payment"
    PAID = "PD", "Paid"
    SHIPPED = "SD", "Shipped"
    COMPLETED = "CO", "Completed"
    CANCELLED = "CA", "Cancelled"


class PaymentMethod(models.TextChoices):
    CARD = "CA", "Card"
    PAY_PAL = "PP", "PayPal"


class Order(TimeStampedModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    shipping_address = models.TextField(max_length=5000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PENDING
    )
    payment_method = models.CharField(
        max_length=2,
        choices=PaymentMethod.choices,
        default=PaymentMethod.PAY_PAL,
        editable=False,
    )
    invoice = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, auto_created=True
    )

    def __str__(self):
        return f"Order - {self.id}"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Order Item - {self.id}"
