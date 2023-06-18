from django.contrib import admin
from .models import UserCard,UserPrivateInfo

# Register your models here.
admin.site.register(UserCard)
admin.site.register(UserPrivateInfo)