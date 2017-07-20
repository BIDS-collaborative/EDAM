"""
This module defines how URLs should route to views.
"""
from django.conf.urls import url

from . import views

# pylint: disable=invalid-name

app_name = 'homepage'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
