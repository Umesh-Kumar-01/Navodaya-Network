from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from .models import UserCard, UserPrivateInfo
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, EditPrivateInfoForm, EditProfileForm
from mysite.constants import JNV_MAP_LIST,STATES
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
import json
from .decorators import verified_user_required

# Create your views here.
def index(request):
    return render(request,'index.html')

@verified_user_required
def profile(request, username):
    # Get the user's profile details based on the provided username
    user = get_object_or_404(User, username=username)
    user_card = get_object_or_404(UserCard, user=user)
    user_private_info = get_object_or_404(UserPrivateInfo, user=user)

    # Check if the current user is viewing their own profile
    is_own_profile = request.user == user

    context = {
        'user':user,
        'user_card': user_card,
        'user_private_info': user_private_info,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'profile.html', context)

@verified_user_required
def edit_profile(request):
    user_card = UserCard.objects.get(user=request.user)
    user_private_info = UserPrivateInfo.objects.get(user=request.user)
    
    if request.method == 'POST':
        card_form = EditProfileForm(request.POST, request.FILES, instance=user_card)
        private_info_form = EditPrivateInfoForm(request.POST, instance=user_private_info)
        
        if card_form.is_valid() and private_info_form.is_valid():
            if card_form.has_changed() or private_info_form.has_changed():
                with transaction.atomic():
                    if card_form.has_changed():
                        card_form.save()  # Save the UserCard model instance
                    if private_info_form.has_changed():
                        private_info_form.save()  # Save the UserPrivateInfo model instance
                        messages.success(request,"Profile has been changed successfully.")
                return redirect('profile', username=request.user.username)
    else:
        card_form = EditProfileForm(instance=user_card)
        private_info_form = EditPrivateInfoForm(instance=user_private_info)
    
    context = {
        'user_private_info':user_private_info,
        'profile_form': card_form,
        'private_info_form': private_info_form,
        'user_card': user_card,
        'STATES':STATES,
    }
    return render(request, 'edit_profile.html', context)


def signup(request):
    if request.user.is_authenticated:
        messages.warning(request,"Redirecting to Home Page...\nYou cannot access Sign up page while being logged In. Please Log out first!")
        return render(request,'index.html')
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'index' with the name of your index view
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request,f"{field_name}: {error}")
    else:
        form = SignUpForm()
    
    json_jnv_list = json.dumps(JNV_MAP_LIST)
    return render(request, 'signup.html', {'form': form,'jnv_data_json':json_jnv_list})

@verified_user_required
def search(request):
    fname = request.GET.get('fname')
    lname = request.GET.get('lname')
    username = request.GET.get('username')
    jnv = request.GET.get('jnv')
    role = request.GET.get('role')
    year = request.GET.get('year')
    query = Q()

    if fname is not None:
        query &= Q(user__first_name__icontains=fname)

    if lname is not None:
        query &= Q(user__last_name__icontains=lname)

    if username is not None:
        query &= Q(user__username__icontains=username)

    if jnv is not None:
        query &= Q(jnv_name__icontains=jnv)

    if role is not None and role != '':
        query &= Q(role=role)

    if year is not None and year != '':
        query &= Q(year=year)
    context = UserCard.objects.filter(query).order_by('user_id')
    paginator = Paginator(context, 50)  # Change the number per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'search.html',{'context':page_obj})

@login_required
@verified_user_required
def autocomplete(request):
    user_name = request.GET.get('input','')
    users = User.objects.filter(username__icontains = user_name).values_list('username',flat=True)
    results = list(users)
    print(results)
    return JsonResponse(results,safe=False)

def terms(request):
    return render(request,'terms.html')