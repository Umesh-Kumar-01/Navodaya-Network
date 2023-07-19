from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from .models import Request, Comment
from .forms import RequestForm, CommentForm
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# @login_required
# def helper(request):
#     return render(request,'helper.html')

def get_filtered_requests(user):
    context = {}
    context["Urgent"] = Request.objects.filter(request_type=Request.URGENT).order_by('created_at')
    context["High_priority"] = Request.objects.filter(request_type=Request.HIGH_PRIORITY).order_by('created_at')
    context["Normal"] = Request.objects.filter(request_type=Request.NORMAL).order_by('created_at')
    context["Your_requests"] = Request.objects.filter(created_by__username=user.username).order_by('created_at')
    return context
    
@login_required
def helper(request):
    context = get_filtered_requests(request.user)
    # for x,y in context.items():
    #     print(x,len(y))
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.created_by = request.user
            new_request.save()
            expire_time = new_request.EXPIRATION_PERIODS.get(new_request.request_type,'N')
            
            new_request.deletion_at = new_request.created_at + timedelta(days=expire_time)
            new_request.save()
            messages.success(request,"Request Submitted Successfully!") # New Message needs to implement
        
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request,f"{field_name}: {error}")
    else:
        form = RequestForm()
    
    return render(request,'helper.html',{'form':form,"context":context})

@login_required
def view_request(request, request_id):
    help_request = get_object_or_404(Request, help_id=request_id)
    if request.method == "POST":
        request.POST = request.POST.copy()
        if request.POST['private_text']!="":
            request.POST['text']=request.POST['private_text']
        print(request.POST)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.request = help_request
            comment.created_by = request.user
            comment.save()
        print(form.errors)
    else:
        form = CommentForm()
    comments = Comment.objects.filter(request=help_request).order_by("created_at")
    return render(request, 'request.html', {"help": help_request, "comments": comments, "form": form})