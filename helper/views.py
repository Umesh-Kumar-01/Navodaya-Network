from django.shortcuts import render,redirect,HttpResponse
from .models import *
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def helper(request):
    return render(request,'helper.html')