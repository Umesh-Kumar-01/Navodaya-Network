from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('request/<int:request_id>/',views.view_request,name="view_request"),
    path('request/<int:request_id>/subscribe_for_updates/', views.subscribe_for_updates, name='subscribe_for_updates'),
    path('request/<int:request_id>/unsubscribe_from_updates/', views.unsubscribe_from_updates, name='unsubscribe_from_updates'),
    path('request/<int:request_id>/close/', views.close_request, name='close_request'),
    path('',views.helper,name="helper"),
    path('request/<int:request_id>/delete/', views.delete_request, name='delete_request'),
]
