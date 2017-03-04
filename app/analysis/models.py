from __future__ import unicode_literals

from django.db import models

# Create your models here.

class PierData(models.Model):
  name = models.TextField(primary_key=True)
  json = models.TextField()