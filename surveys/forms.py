# surveys/forms.py

from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['heading', 'description', 'google_form_link','expire_on']
