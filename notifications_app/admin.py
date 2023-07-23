from django.contrib import admin
from .models import BroadcastNotification, Notification

# Register your models here.
admin.site.register(BroadcastNotification)
admin.site.register(Notification)