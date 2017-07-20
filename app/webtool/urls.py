"""
This module defines how URLs should route to views.
"""
from django.conf.urls import url

from . import views

# pylint: disable=invalid-name

app_name = 'webtool'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    # model selection API returns data for all plots
    url(r'^model_selection/', views.model_selection),
]
