import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Template, Context


class InfoPanelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("info-panel", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("info-panel", self.channel_name)

    async def send_message(self, event):
        product_url, product_name = event["message"]

        template = Template(
            """
            <div class="alert alert-info" role="alert">
              ➕ Someone just subscribed to <a href="{{ url }}" class="alert-link">«{{ name }}»</a>
            </div>
            """
        )

        context = Context({"url": product_url, "name": product_name})

        rendered_message = template.render(context)

        await self.send(
            text_data=json.dumps({"message": rendered_message, "type": "info"})
        )
