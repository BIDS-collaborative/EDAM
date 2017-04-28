from __future__ import unicode_literals

from django.db import models

# Create your models here.

# model for caching analysis plots in database
class PierData(models.Model):
  name = models.TextField(primary_key=True)
  json = models.TextField()