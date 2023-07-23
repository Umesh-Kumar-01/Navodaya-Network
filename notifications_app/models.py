from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json
from django.contrib.auth.models import User
# from .tasks import send_notification_task

# Create your models here.
class BroadcastNotification(models.Model):
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    notify_url = models.URLField(blank=True,null=True)

    class Meta:
        ordering = ['user','-timestamp']