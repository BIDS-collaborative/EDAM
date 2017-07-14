"""
This module defines the application's views, which are needed to render pages.
"""
from django.shortcuts import render

def index(request):
    """
    renders the page with html
    """
    return render(request, 'homepage.html')
