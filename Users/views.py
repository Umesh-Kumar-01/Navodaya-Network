from django.shortcuts import render,redirect,HttpResponse
from .models import UserCard, UserPrivateInfo
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from mysite.constants import JNV_MAP_LIST

# Create your views here.
def index(request):
    print(request.POST)
    error_message = []
    return render(request,'index.html',{'dangerMessages': error_message})

def signup(request):
    if request.user.is_authenticated:
        dangerMessages = ["Redirecting to Home Page...\nYou cannot access Sign up page while being logged In. Please Log out first!"]
        return render(request,'index.html',{'dangerMessages':dangerMessages})
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'index' with the name of your index view
        else:
            dangerMessage = ""
            for field_name, errors in form.errors.items():
                for error in errors:
                    dangerMessage += f"{field_name}: {error}\n"
            return render(request, 'your_template.html', {'form': form, 'dangerMessages': [dangerMessage]})
        #     return HttpResponse("There is an Error!")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def search(request):
    return render(request,'search.html')

@login_required
def notification(request):
    return render(request,'notification.html')