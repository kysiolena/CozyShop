# Send message to Info Panel when SubscribeProduct create
import json

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.urls import reverse

from cart.consumers import InfoPanelConsumer
from catalog.models import Product


@shared_task
def send_notification_task(product_id: int):
    if not product_id:
        return

    # Get Product by ID
    product = Product.objects.get(id=product_id)

    # Get Channel Layer
    chanel_layer = get_channel_layer()

    # Create event data
    event = {
        "type": "send_notification_handler",
        "product_data": json.dumps(
            {
                "url": reverse("product_page", kwargs={"slug": product.slug}),
                "name": product.name,
            }
        ),
    }

    # Send event to group handler
    async_to_sync(chanel_layer.group_send)(
        InfoPanelConsumer.group_name,
        event,
    )

    return f"Sent notification about product «{product.name}»"
