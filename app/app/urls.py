"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
"""
from django.conf.urls import url, include
from django.contrib import admin

# pylint: disable=invalid-name

urlpatterns = [
    url(r'^$', include('homepage.urls'), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^webtool/', include('webtool.urls')),
    url(r'^analysis/', include('analysis.urls'))
]
