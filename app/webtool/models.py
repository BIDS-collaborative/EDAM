"""
Model definitions.

This module defines how information used by the web app is structured and how the
Python layer interfaces with a database.
"""
from __future__ import unicode_literals

from django.db import models

class Document(models.Model):
    """
    model for file upload
    """
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    label = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
