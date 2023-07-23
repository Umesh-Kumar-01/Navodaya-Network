from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .tasks import broadcast_notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from .models import Notification, BroadcastNotification

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-timestamp')
    broadcast_notifications = BroadcastNotification.objects.all().order_by('-broadcast_on')[:5]
    all_notifications = list(notifications) + list(broadcast_notifications)
    all_notifications.sort(key=lambda x: x.timestamp if hasattr(x, 'timestamp') else x.broadcast_on, reverse=True)

    context = {'notifications': all_notifications}
    print(context)
    return render(request, 'notification.html', context)

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect('notification')

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('notification')

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
