from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_list, name='survey_list'),  # URL for displaying the list of surveys and creating new survey
    path('survey/<int:pk>/', views.survey_detail, name='survey_detail'),  # URL for survey detail page
]
