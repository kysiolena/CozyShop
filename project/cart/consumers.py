import json
from typing import TypedDict

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string


class TSendNotificationEvent(TypedDict):
    type: str
    product_data: str


class InfoPanelConsumer(AsyncWebsocketConsumer):
    group_name = "info-panel"
    user = None

    async def connect(self):
        self.user = self.scope["user"]

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification_handler(self, event: TSendNotificationEvent):
        product = json.loads(event["product_data"])

        message = render_to_string(
            "cart/blocks/info-panel-message.html",
            context={"url": product["url"], "name": product["name"]},
        )

        await self.send(text_data=json.dumps({"message": message}))
