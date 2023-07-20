# surveys/models.py

from django.db import models
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User

def validate_survey_link(value):
    # Regular expressions to match Google Forms and SurveyMonkey URLs
    google_form_pattern = r'^https:\/\/docs\.google\.com\/forms\/d\/[\w\-]+\/viewform$'
    surveymonkey_pattern = r'^https:\/\/www\.surveymonkey\.com\/r\/[\w\-]+$'

    # Check if the URL matches the Google Forms or SurveyMonkey patterns
    if not re.match(google_form_pattern, value) and not re.match(surveymonkey_pattern, value):
        raise ValidationError('Invalid survey link. Please provide a valid Google Forms or SurveyMonkey link.')

class Survey(models.Model):
    heading = models.CharField(max_length=200)
    description = models.TextField()
    google_form_link = models.URLField(validators=[validate_survey_link])
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_surveys', default=1)
    respondents = models.ManyToManyField(User, related_name='filled_surveys', blank=True)

    def __str__(self):
        return self.heading
    
    def total_respondents(self):
        return self.respondents.count()
