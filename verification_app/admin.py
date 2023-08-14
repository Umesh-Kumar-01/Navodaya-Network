from django.contrib import admin
from .models import POCRequest,Verification, SchoolPOCs

# Register your models here.
admin.site.register(Verification)
admin.site.register(POCRequest)
admin.site.register(SchoolPOCs)


