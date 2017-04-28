from __future__ import unicode_literals

from django.db import models

# Create your models here.

# model for file upload
class Document(models.Model):
  description = models.CharField(max_length=255, blank=True)
  document = models.FileField(upload_to='documents/')
  label = models.FileField(upload_to='documents/')
  uploaded_at = models.DateTimeField(auto_now_add=True)