from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

def index(request):
    # respond with template with context
    return render(request, 'homepage.html')
