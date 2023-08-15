from django.contrib import admin
from .models import Announcement, AnnouncementGroup

# Register your models here.
admin.site.register(Announcement)
admin.site.register(AnnouncementGroup)
