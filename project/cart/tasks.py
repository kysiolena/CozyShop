# Send message to Info Panel when SubscribeProduct create
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.urls import reverse

from catalog.models import Product
from subscribe.consumers import InfoPanelConsumer


@shared_task
def send_notification_task(product_id: int):
    if not product_id:
        return

    # Get Product by ID
    product = Product.objects.get(id=product_id)

    # Get Channel Layer
    chanel_layer = get_channel_layer()

    # Send message to group
    async_to_sync(chanel_layer.group_send)(
        InfoPanelConsumer.group_name,
        {
            "type": "send_notification",
            "message": (
                reverse("product_page", kwargs={"slug": product.slug}),
                product.name,
            ),
        },
    )
