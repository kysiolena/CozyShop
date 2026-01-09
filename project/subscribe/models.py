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


# # Send email when in_stock flag of Product change (only Subscribed users)
# def send_email_when_update_product_in_stock(
#     sender, instance, created, update_fields, **kwargs
# ):
#     if not created and update_fields:
#         # Send email logic (TO DO: celery)
#         print("Send email logic (TO DO: celery)", update_fields)
#
#
# post_save.connect(send_email_when_update_product_in_stock, sender=Product)
