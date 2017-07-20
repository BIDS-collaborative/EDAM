"""
Model definitions.

This module defines how information used by the web app is structured and how the
Python layer interfaces with a database.
"""

from __future__ import unicode_literals

from django.db import models

class PierData(models.Model):
    """
    model for caching analysis plots in database
    """
    name = models.TextField(primary_key=True)
    json = models.TextField()
    