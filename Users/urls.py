from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('home/',views.index,name='index'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('signup/',views.signup,name='signup'),
    path('search/',views.search,name='search'),
    path('notification/',views.notification,name='notification'),
    path('autocomplete/',views.autocomplete,name='autocomplete'),
    path('',RedirectView.as_view(url='home/'))
]
