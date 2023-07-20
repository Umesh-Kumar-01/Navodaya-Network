from django.db import models

# Create your models here.
from django.db import models

class Survey(models.Model):
    heading = models.CharField(max_length=200)
    description = models.TextField()
    google_form_link = models.URLField()

    def __str__(self):
        return self.heading