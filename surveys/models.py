# surveys/models.py

from django.db import models
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
from django.utils import timezone

def validate_survey_link(value):
    # Regular expressions to match Google Forms and SurveyMonkey URLs
    google_form_pattern = r'^https:\/\/(docs\.google\.com\/forms\/d\/|forms.gle\/)?'
    surveymonkey_pattern = r'^https:\/\/(www\.)?surveymonkey\.com\/r\/[\w\-]+$'

    # Check if the URL matches the Google Forms or SurveyMonkey patterns
    if not re.match(google_form_pattern, value) and not re.match(surveymonkey_pattern, value):
        print("Link Doesn't match!",value)
        raise ValidationError('Invalid survey link. Please provide a valid Google Forms or SurveyMonkey link.')

class Survey(models.Model):
    heading = models.CharField(max_length=200)
    description = models.TextField()
    google_form_link = models.URLField(validators=[validate_survey_link])
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_surveys', default=1)
    respondents = models.ManyToManyField(User, related_name='filled_surveys', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    expire_on = models.DateTimeField(null=True,blank=True)
    is_completed = models.BooleanField(default=False)
    is_special = models.BooleanField(default=False)

    def __str__(self):
        return self.heading
    
    def total_respondents(self):
        return self.respondents.count()
