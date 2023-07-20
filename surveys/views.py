from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Survey
from .forms import SurveyForm
from django.contrib import messages

@login_required
def survey_list(request):
    if request.method == 'POST':
        # This is the view to handle the creation of a new survey
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.creator = request.user
            survey.save()
            form.save_m2m()  # Save the many-to-many relationship
            messages.success("Survey uploaded successfully!")
            return redirect('survey_list')
        else:
            messages.error("Form is invalid! Please check the form once. Only google form and surveymonkey links allowed.")
    else:
        # This is the view to display the list of surveys
        surveys = Survey.objects.all()
        form = SurveyForm()
        return render(request, 'surveys/survey_list.html', {'surveys': surveys, 'form': form})

@login_required
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == "POST":
        response_user = request.user
        if response_user in survey.respondents.all():
            messages.warning(request, "You have already filled the survey!")
        else:
            survey.respondents.add(response_user)
            messages.success(request, "Response has been recorded!")

    return render(request, 'surveys/survey_detail.html', {'survey': survey})

