from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mysite.constants import JNV_MAP_LIST
import uuid

class SchoolPOCs(models.Model):
    ROLE_CHOICES = (
        ('T', 'Teacher'),
        ('A', 'Alumnus/Alumna'),
        ('W', 'Worker'),
        ('S', 'Student'),
        ('O', 'Office Member'),
    )
    jnv_name = models.CharField(max_length = 50,choices=[(w,"Jawahar Navodaya Vidyalaya, "+w) for y in JNV_MAP_LIST.values() for w in y])
    role_name = models.CharField(max_length=1, choices=ROLE_CHOICES)
    batch_year = models.PositiveIntegerField(blank=True,null=True)
    pocs = models.ManyToManyField(User)

class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user")
    
    is_verified_email = models.BooleanField(default=False)
    is_verified_by_poc = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    jnv_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    verified_by = models.OneToOneField(User, on_delete=models.RESTRICT,related_name="verified_by", blank=True, null=True)

    def __str__(self):
        return f"Verification for {self.user.username}"

class POCRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    documents = models.FileField(upload_to='poc_documents/')
    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)