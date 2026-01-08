from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse_lazy

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


# Send message to Info Panel when SubscribeProduct create
def send_message_to_info_panel_when_create_subscribe_product(
    sender, instance, created, **kwargs
):
    if created:
        # Send message to Info Panel when SubscribeProduct create (TO DO: celery)
        chanel_layer = get_channel_layer()
        async_to_sync(chanel_layer.group_send)(
            "info-panel",
            {
                "type": "send_message",
                "message": (
                    reverse_lazy(
                        "product_page", kwargs={"slug": instance.product.slug}
                    ),
                    instance.product.name,
                ),
            },
        )


post_save.connect(
    send_message_to_info_panel_when_create_subscribe_product, sender=SubscribeProduct
)
