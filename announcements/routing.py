# announcements/routing.py

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/announcements/$', consumers.AnnouncementConsumer.as_asgi()),
    # Add other WebSocket routes if needed
]
