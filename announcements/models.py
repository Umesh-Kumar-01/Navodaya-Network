from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AnnouncementGroup(models.Model):
    name = models.CharField(max_length=100)
    administrators = models.ManyToManyField(User, related_name='admin_groups')
    
class Announcement(models.Model):
    group = models.ForeignKey(AnnouncementGroup, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    read_by = models.ManyToManyField(User, related_name='read_announcements')
    
