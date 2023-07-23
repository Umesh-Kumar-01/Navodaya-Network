from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('home/',views.index,name='index'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('signup/',views.signup,name='signup'),
    path('search/',views.search,name='search'),
    path('autocomplete/',views.autocomplete,name='autocomplete'),
    path('',RedirectView.as_view(url='home/'))
]
