from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Survey
from .forms import SurveyForm
from django.contrib import messages
from django.http import HttpResponseForbidden


@login_required
def survey_list(request):
    surveys = Survey.objects.all()

    if request.method == 'POST':
        # Check if the current user has reached the maximum limit of uncompleted surveys
        if not request.user.is_superuser:
            uncompleted_surveys = surveys.filter(creator=request.user, is_completed=False)
            if uncompleted_surveys.count() >= 3:
                messages.error(request, "Maximum limit for survey submission is 3. Complete or delete previous surveys to add more.")
                return redirect('survey_list')

        form = SurveyForm(request.POST)
        if form.is_valid():
            # Check if the provided expiration date is valid
            expire_on = form.cleaned_data.get('expire_on')
            if expire_on:
                current_time = timezone.now()
                if expire_on <= current_time:
                    messages.error(request, "Please provide a valid expiration date in the future.")
                    return redirect('survey_list')
            
            survey = form.save(commit=False)
            survey.creator = request.user
            survey.save()
            form.save_m2m()  # Save the many-to-many relationship
            messages.success(request, "Survey uploaded successfully!")
            return redirect('survey_list')
        else:
            messages.error(request, "Form is invalid! Please check the form once. Only Google Form and SurveyMonkey links allowed.")
    else:
        # This is the view to display the list of surveys
        form = SurveyForm()

    # Check and mark surveys as complete based on expiration date
    current_time = timezone.now()
    for survey in surveys:
        if survey.expire_on and current_time > survey.expire_on and not survey.is_completed:
            survey.is_completed = True
            survey.save()
            # Perform actions on survey completion (e.g., delete files from the server)

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

@login_required
def delete_survey(request, survey_id):
    # Fetch the survey using the survey_id, or return 404 if not found
    survey = get_object_or_404(Survey, id=survey_id, creator=request.user)

    if request.method == 'POST':
        # Handle the delete confirmation
        if survey.expire_on and timezone.now() >= survey.expire_on:
            messages.error(request, "Survey has Expired!. You cannot delete it Now.")
        else:
            # Perform any additional actions before deletion (e.g., delete files from the server)
            survey.delete()
            messages.success(request, "Survey deleted successfully.")
            return redirect('survey_list')

    return redirect('survey_list')

@login_required
def mark_as_complete(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, creator=request.user)

    if not survey.is_completed:
        # Perform any actions when marking the survey as complete
        survey.is_completed = True
        survey.save()
        messages.success(request, "Survey marked as complete.")
    else:
        return HttpResponseForbidden("Cannot mark the survey as complete.")

    return redirect('survey_list')