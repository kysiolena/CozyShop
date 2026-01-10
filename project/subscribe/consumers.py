import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Template, Context


class InfoPanelConsumer(AsyncWebsocketConsumer):
    group_name = "info-panel"

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        product_url, product_name = event["message"]

        template = Template(
            """
            <div class="alert alert-info alert-dismissible show fade" role="alert">
              <div>
                ➕ Someone just added to cart the <a href="{{ url }}" class="alert-link">«{{ name }}» product!</a>
              </div>
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            """
        )

        context = Context({"url": product_url, "name": product_name})

        rendered_message = template.render(context)

        await self.send(text_data=json.dumps({"message": rendered_message}))
