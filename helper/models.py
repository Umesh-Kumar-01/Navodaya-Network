from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Request(models.Model):
    URGENT = 'U'
    HIGH_PRIORITY = 'H'
    NORMAL = 'N'

    TYPE_CHOICES = (
        (URGENT, 'Urgent'),
        (HIGH_PRIORITY, 'High priority'),
        (NORMAL, 'Normal'),
    )

    EXPIRATION_PERIODS = {
        URGENT: 10,  # Urgent: 10 days
        HIGH_PRIORITY: 20,  # High priority: 20 days
        NORMAL: 30,  # Normal: 30 days
    }

    help_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300, default='')
    body = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=4)
    request_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=NORMAL)
    deletion_at = models.DateTimeField(null=True, blank=True)
    profession = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_requests', blank=True)
    is_closed = models.BooleanField(default=False)

    @property
    def is_expired(self):
        if self.deletion_at:
            expired = self.deletion_at <= timezone.now()
            if expired:
                self.is_closed = True
                self.save()
            return expired
        return False

    def get_comments(self):
        return self.comments.order_by('created_at')

    def __str__(self):
        return "Request:" +str(self.help_id)


class Comment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_created', default=4)
    is_special = models.BooleanField(default=False)
    mobile_number = models.IntegerField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    def __str__(self):
        return f"Comment {self.id} - {self.request_id}"
