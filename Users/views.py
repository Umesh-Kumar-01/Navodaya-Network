from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from .models import UserCard, UserPrivateInfo
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from mysite.constants import JNV_MAP_LIST
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')

@login_required
def profile(request, username):
    # Get the user's profile details based on the provided username
    user = get_object_or_404(User, username=username)
    user_card = get_object_or_404(UserCard, user=user)
    user_private_info = get_object_or_404(UserPrivateInfo, user=user)

    # Check if the current user is viewing their own profile
    is_own_profile = request.user == user

    context = {
        'user_card': user_card,
        'user_private_info': user_private_info,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    # Get the user's profile details and private info for editing
    user_card = get_object_or_404(UserCard, user=request.user)
    user_private_info = get_object_or_404(UserPrivateInfo, user=request.user)

    if request.method == 'POST':
        # Process the form data for updating the profile
        # ... Your form processing logic here ...
        # For example, you can use Django forms to handle the form data.

        # After updating, redirect to the user's profile page
        return redirect('profile', username=request.user.username)

    context = {
        'user_card': user_card,
        'user_private_info': user_private_info,
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
            return render(request, 'your_template.html', {'form': form})
        #     return HttpResponse("There is an Error!")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
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
def autocomplete(request):
    user_name = request.GET.get('input','')
    users = User.objects.filter(username__icontains = user_name).values_list('username',flat=True)
    results = list(users)
    print(results)
    return JsonResponse(results,safe=False)