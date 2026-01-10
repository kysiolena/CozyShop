from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Product
from shop.models import TimeStampedModel

UserModel = get_user_model()


class SubscribeProduct(TimeStampedModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product"
    )

    class Meta:
        unique_together = ("user", "product")
