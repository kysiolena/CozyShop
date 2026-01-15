from django.urls import path

from cart.consumers import InfoPanelConsumer

websocket_urlpatterns = [path("ws/info-panel/", InfoPanelConsumer.as_asgi())]
