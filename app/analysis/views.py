from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from webtool.views import handle_uploaded_file

def index(request):
  # load html from templates/
  template = loader.get_template('analysis.html')
  
  # result_dict = handle_uploaded_file("/static/documents/edam_data.csv")
  # respond with template with context
  # return HttpResponse(template.render(request, "webtool_result.html", result_dict))
  return HttpResponse(template.render(request))

@api_view(['GET'])
def test():
  return Response(['test'])


@api_view(['GET'])
def confusion_matrix(request):
  return Response([[0.69, 0.02],[0.03, 0.70]])


@api_view(['GET'])
def feature_importance(request):
  return Response([4, 8, 15, 16, 23, 42, 46, 21, 12])
  
@api_view(['GET'])
def pca_variance(request):
  return Response('test')
  
