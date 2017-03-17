from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Document(models.Model):
  description = models.CharField(max_length=255, blank=True)
  document = models.FileField(upload_to='documents/')
  label = models.FileField(upload_to='documents/')
  uploaded_at = models.DateTimeField(auto_now_add=True)

class Hyperparameter(models.Model):
    CHOICES = (
        ('Logistic Regression', 'Logistic Regression'), 
        ('Random Forest', 'Random Forest')
    )
    model_choice = models.CharField(max_length=255, choices=CHOICES)
    hyperparameters = models.CharField(max_length=255, blank=True)
    filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)