from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import BroadcastNotification, Notification
import json
from celery import Celery, states
from celery.exceptions import Ignore
import asyncio


@shared_task
def send_notification_task(notification_id):
    try:
        notification = Notification.objects.get(pk=notification_id)
        group_name = f"user_{notification.user.id}"
        channel_layer = get_channel_layer()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(channel_layer.group_send(
            group_name,
            {
                'type': 'send_notification',
                'recipient_user_id': notification.user.id,
                'message': json.dumps(
                    notification.message
                ),
            }
        ))
        notification.sent = True
        notification.save()  # Save the notification after updating 'sent' attribute
    except:
        # Handle the case when the notification with the given ID does not exist
        raise Ignore()

@shared_task(bind = True)
def broadcast_notification(self, data):
    # print(data)
    try:
        notification = BroadcastNotification.objects.filter(id = int(data))
        if len(notification)>0:
            notification = notification.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "notification_broadcast",
                {
                    'type': 'send_notification',
                    'message': json.dumps(notification.message),
                }))
            notification.sent = True
            notification.save()
            return 'Done'

        else:
            self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Not Found"}
            )

            raise Ignore()

    except:
        self.update_state(
                state = 'FAILURE',
                meta = {
                        'exe': "Failed"
                        # 'exc_type': type(ex).__name__,
                        # 'exc_message': traceback.format_exc().split('\n')
                        # 'custom': '...'
                    }
            )

        raise Ignore()