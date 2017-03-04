from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

def index(request):
  # load html from templates/
  template = loader.get_template('homepage.html')
  context = {

  }
  # respond with template with context
  return HttpResponse(template.render(context, request))

def indexTest(request):
    # load html from templates/
    template = loader.get_template('homepage.html')
    context = {

    }
    # respond with template with context
    return HttpResponse(template.render(context, request))