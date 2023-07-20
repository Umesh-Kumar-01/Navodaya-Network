# surveys/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Survey
from .forms import SurveyForm

@login_required
def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'surveys/survey_list.html', {'surveys': surveys})

@login_required
def add_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_list')
    else:
        form = SurveyForm()
    return render(request, 'surveys/add_survey.html', {'form': form})
