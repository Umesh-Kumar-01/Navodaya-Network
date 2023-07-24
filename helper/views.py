from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from .models import Request, Comment
from .forms import RequestForm, CommentForm
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps


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
            new_request.subscribers.add(request.user)
            new_request.save()
            messages.success(request,"Request Submitted Successfully!") # New Message needs to implement
        
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request,f"{field_name}: {error}")
    else:
        form = RequestForm()
    
    return render(request,'helper.html',{'form':form,"context":context})

def check_expired(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        help_request = get_object_or_404(Request, help_id=kwargs['request_id'])
        if (not help_request.is_closed) and help_request.is_expired:
            # Handle the expired request here (e.g., redirect or show a message)
            Comment.objects.create(text="The request has expired, so the system is automatically closing it.\nIf it hasn't been resolved, please create a fresh request and select an appropriate type, such as urgent, high priority, or normal.",request=help_request) # deafult creator admin
            messages.warning(request,'This request has been expired!')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@check_expired
def view_request(request, request_id):
    help_request = get_object_or_404(Request, help_id=request_id)
    if request.method == "POST":
        request.POST = request.POST.copy()
        if request.POST['private_text']!="":
            request.POST['text']=request.POST['private_text']
        # print(request.POST)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.request = help_request
            comment.created_by = request.user
            comment.save()
        # print(form.errors)
    else:
        form = CommentForm()
    comments = Comment.objects.filter(request=help_request).order_by("created_at")
    return render(request, 'request.html', {"help": help_request, "comments": comments, "form": form})

@login_required
def close_request(request, request_id):
    help_request = get_object_or_404(Request, help_id=request_id)
    
    if request.method == "GET" and not help_request.is_closed:
        help_request.is_closed = True
        help_request.save()
        Comment.objects.create(text="The User has closed the request. Thank you for being a part of it!",request=help_request) # deafult creator admin
        messages.success(request, "Request closed successfully!")
    elif help_request.is_closed:
        messages.warning(request, "Request is already Closed!")
    
    return redirect('view_request', request_id=help_request.help_id)

@login_required
def delete_request(request, request_id):
    help_request = get_object_or_404(Request, help_id=request_id)

    if help_request.created_by == request.user:
        if help_request.is_closed:
            messages.warning(request,'Request is already Closed! You can not delete Now.')
        else:
            help_request.delete()
            messages.success(request,'Request is deleted successfully!')  # Redirect to the list of requests after successful deletion
    else:
        # Handle unauthorized deletion attempt (e.g., show an error message)
        messages.error(request,"UnAuthorised Deletion Request!")
    return redirect('helper')

@login_required
def subscribe_for_updates(request, request_id):
    # Get the request object from the database
    request_obj = Request.objects.get(pk=request_id)
    
    # Check if the current user is not already subscribed
    if request.user not in request_obj.subscribers.all():
        # Add the current user to the subscribers list
        request_obj.subscribers.add(request.user)
    
    # Redirect back to the detail view of the request
    return redirect('view_request', request_id=request_id)

@login_required
def unsubscribe_from_updates(request, request_id):
    # Get the request object from the database
    request_obj = Request.objects.get(pk=request_id)
    
    # Check if the current user is subscribed
    if request.user in request_obj.subscribers.all():
        # Remove the current user from the subscribers list
        request_obj.subscribers.remove(request.user)
    
    # Redirect back to the detail view of the request
    return redirect('view_request', request_id=request_id)