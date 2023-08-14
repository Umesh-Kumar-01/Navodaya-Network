from django.urls import path
from . import views

urlpatterns = [
    path("poc/<str:token>/",views.jnv_verify, name="jnv_verify_link"),
    path('apply-poc/', views.apply_poc, name='apply_poc'),
    path("<str:token>/",views.verify_email, name="email_verify_link"),
    path("send_link", views.send_verification_code, name="send_verification_link"),
    path('', views.verify, name='verify'),
]
