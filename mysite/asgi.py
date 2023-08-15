"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import get_channel_layer
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddleware, AuthMiddlewareStack
from notifications_app.routing import websocket_urlpatterns as notifications_websockets
from announcements.routing import websocket_urlpatterns as announcements_websockets

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(notifications_websockets + announcements_websockets)
    ),
})
