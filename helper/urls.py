from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('',views.helper,name="helper"),
    path('request/<int:request_id>/',views.view_request,name="view_request")
]
