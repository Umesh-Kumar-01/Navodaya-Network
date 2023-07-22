from django.shortcuts import render, HttpResponse
from .tasks import broadcast_notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            "type":"send_notification",
            "message": "notification"
        }
    )
    return HttpResponse("Done")