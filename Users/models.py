from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MaxLengthValidator, FileExtensionValidator
from mysite.constants import JNV_MAP_LIST, STATES
from django.contrib.auth.models import User

# Create your models here.
class UserCard(models.Model):
    class RegionName(models.TextChoices):
        BHOPAL = 'BP',_('Bhopal')
        CHANDIGARH = 'CH',_('Chandigarh')
        HYDERABAD = 'HB',_('Hyderabad')
        JAIPUR = 'JP',_('Jaipur')
        LUCKNOW = 'LK',_('Lucknow')
        PATNA = 'PT',_('Patna')
        PUNE = 'PN',_('Pune')
        SHILLONG = 'SH',_('Shillong')
    
    ROLE_CHOICES = (
        ('T', 'Teacher'),
        ('A', 'Alumnus/Alumna'),
        ('W', 'Worker'),
        ('S', 'Student'),
        ('O', 'Office Member'),
    )
    
    
    default_region_name = "JP" # default 
    
    user = models.OneToOneField(User, on_delete=models.RESTRICT, primary_key=True)
    region_name = models.CharField(max_length =2, choices=RegionName.choices)
    jnv_name = models.CharField(max_length = 50,choices=[(w,"Jawahar Navodaya Vidyalaya, "+w) for y in JNV_MAP_LIST.values() for w in y])
    
    verified = models.BooleanField(default=False)
    role = models.CharField(max_length=1,choices=ROLE_CHOICES)
    year = models.PositiveIntegerField(blank=True,null=True)
    HomeTown = models.CharField(max_length=300,blank=True,null=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        default='default_profile.png',
        validators=[
            MaxLengthValidator(limit_value=100 * 1024, message="The image size should be less than 100KB."),
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'], message="Only PNG and JPG files are allowed."),
            # ... Other validators if needed ...
        ]
    )
    def __str__(self) -> str:
        return "Public Data User:"+self.user.username
    
class UserPrivateInfo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.RESTRICT, primary_key=True)
    current_location_city = models.CharField(max_length=300,blank=True,null=True)
    current_location_state = models.CharField(max_length=40,choices =[(x,x) for x in STATES],blank=True,null=True)
    current_location_zip = models.PositiveIntegerField(blank=True,null=True)
    profession = models.CharField(max_length=60,blank=True,null=True)
    
    def __str__(self) -> str:
        return "Private Data User:"+self.user.username
