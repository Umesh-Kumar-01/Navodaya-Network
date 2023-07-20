from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('add/', views.add_survey, name='add_survey'),
]