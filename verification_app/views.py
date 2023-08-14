# views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Verification, POCRequest, SchoolPOCs
from django.utils import timezone
import random
import string
from .tasks import send_verification_email
from django.conf import settings
from django.contrib import messages

@login_required
def send_verification_code(request):
    verification = Verification.objects.get(user=request.user)
    if not verification.is_verified_email:
        subject = 'Email Verification Code'
        message = f"Dear {request.user.username},\n\nThank you for using our verification system. Verification link: http://127.0.0.1:8000/verify/{verification.email_verification_token} \n\nPlease visit this link to proceed.\n\nIf you didn't request this link, please ignore this email.\n\nBest regards,\nThe Verification Team - Navodaya Network."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]

        # Use the Celery task to send the email asynchronously
        try:
            send_verification_email.delay(subject, message, from_email, recipient_list)
            messages.success(request,f"Verification Email has been sent successfully to {request.user.username}.")
        except Exception as e:
            messages.error(request,f"There was an error in Email. Please check your email again! {e}")
            

    return redirect('verify')

@login_required
def verify(request):
    print(request.method)
    print(request)
    verification, created = Verification.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Sending request to respective POCs
        role = request.user.usercard.role
        try:
            if role=='S':
                poc = SchoolPOCs.objects.get(jnv_name=request.user.usercard.jnv_name, role_name=role, batch_year=request.user.usercard.year)
            else:
                poc = SchoolPOCs.objects.get(jnv_name=request.user.usercard.jnv_name, role_name=role)
        except:
            poc = None
        
        if poc:
            subject = f'JNV Verification Request of {verification.user.username}'
            message = f"Dear {verification.user.username},\n\nThank you for being a part of our verification Team.\n\n There is new request...\n\nName: {verification.user.username}\nJNV: {verification.user.usercard.jnv_name}\nRole: {verification.user.usercard.role}\nBatch Year: {verification.user.usercard.year}\nProfile Page Link:{request.build_absolute_uri(reverse('profile',args=[verification.user.username]))}\n\n Visit This link to verify: http://127.0.0.1:8000/verify/poc/{verification.jnv_verification_token}\n\n Regards\nNavodaya Network"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [x.email for x in poc.pocs.all()]
            
            send_verification_email.delay(subject,message,from_email,recipient_list)
            
            messages.success(request,"Your verification request is sent to the respective POC")
        else:
            messages.warning(request,"There is no POC till now. To verify yourself and add others please take the initiative and fill the form for POC.")
            
    print(verification)
    return render(request,'verify.html',context={'verification':verification})
        
@login_required
def verify_email(request, token):
    try:
        verification = Verification.objects.get(email_verification_token=token)
        if verification:
            verification.is_verified_email = True
            verification.save()
            
            messages.success(request, f"Email Verification is done!")
            
    except Verification.DoesNotExist:
        messages.error(request, "Invalid verification token.")

    return redirect('verify')

@login_required
def jnv_verify(request, token):
    try:
        verification = Verification.objects.get(jnv_verification_token=token)
        if verification and verification.is_verified_email:
            if verification.is_verified_by_poc:
                message.warn(request, f"User is already verified by {verification.verified_by}.")
                return redirect('index')
            
            verification.is_verified_by_poc = True
            verification.verified_by = request.user
            verification.save()
            verification.user.usercard.is_verified = True
            verification.user.usercard.save()
            # send mail to user
            subject = 'JNV Verification Status: PASSED!'
            message = f"Dear {verification.user.username},\n\nThank you for using our verification system. You JNV Verification is done and you are verified by {request.user} \n\n Now you can visit and the website and avail all the services.\n\nIf you didn't request this, please ignore this email.\n\nBest regards,\nThe Verification Team - Navodaya Network."
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [verification.user.email]
            
            send_verification_email.delay(subject,message,from_email,recipient_list)
            
            messages.success(request, f"JNV Verification of {verification.user.username} is done!")
        
    except Verification.DoesNotExist:
        messages.error(request, "Invalid verification token.")

    return redirect('index')

@login_required
def apply_poc(request):
    verification = Verification.objects.get(user=request.user)
    if verification.is_verified_email and not verification.is_verified_by_poc:
        if request.method == 'POST':
            documents = request.POST.get('documents')
            newobj = POCRequest.objects.create(user=request.user, school=request.user.usercard.jnv_name,documents=documents)
            newobj.save()
            messages.success(request, "Your request has been forwarded to review!")
            return redirect('verify')
    else:
        return redirect('verify')

    return render(request, 'apply_poc.html')
