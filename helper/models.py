from django.db import models
from django.contrib.auth.models import User
from datetime import date

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    request_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=NORMAL)
    deletion_at = models.DateTimeField(null=True, blank=True)
    profession = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def is_expired(self):
        if self.deletion_date:
            return self.deletion_at <= date.today()
        return False

    def get_comments(self):
        return self.comments.order_by('created_at')

    def __str__(self):
        return "Request:" +str(self.help_id)


class Comment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_created')
    is_special = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment {self.id} - {self.request_id}"
