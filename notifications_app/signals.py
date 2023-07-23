from .models import Notification, BroadcastNotification
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json
from .tasks import send_notification_task

@receiver(post_save, sender=Notification)
def send_notification_to_user(sender, instance, created, **kwargs):
    if created:
        send_notification_task.delay(instance.id)  # Call the task asynchronously with notification_id

@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        print("Hello")
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="notifications_app.tasks.broadcast_notification", args=json.dumps((instance.id,)))

    #if not created: