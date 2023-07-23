from celery import shared_task
from notifications_app.models import Notification
from django.contrib.auth.models import User

@shared_task
def create_comment_notification_task(message, url, subscribers_data):
    for subscriber_data in subscribers_data:
        user = User.objects.get(id=subscriber_data['id'])
        username = subscriber_data['username']
        Notification.objects.create(
            user=user,
            message=f"Hey {username}! {message}",
            notify_url=url,
        )