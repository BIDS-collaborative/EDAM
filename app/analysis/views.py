from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from webtool.views import handle_uploaded_file

def index(request):
  # load html from templates/
  template = loader.get_template('analysis.html')
  
  result_dict = handle_uploaded_file("/static/documents/edam_data.csv")
  # respond with template with context
  return HttpResponse(template.render(request, "webtool_result.html", result_dict))