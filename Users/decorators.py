from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def verified_user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.usercard.verified:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse('verify'))
    return _wrapped_view
