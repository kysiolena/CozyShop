"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf import settings
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Init Django app
django_application = get_asgi_application()

# After Django app init
from . import urls

application = ProtocolTypeRouter(
    {
        "http": (
            get_asgi_application()
            if settings.IS_PRODUCTION
            else ASGIStaticFilesHandler(get_asgi_application())
        ),
        "websocket": URLRouter(urls.websocket_urlpatterns),
    }
)
