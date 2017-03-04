from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.templatetags.static import static

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import numpy as np
import itertools
import matplotlib.pyplot as plt
import sklearn
import os
import cPickle
from mpl_toolkits.mplot3d import Axes3D
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix


from webtool.views import handle_uploaded_file


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
  # load html from templates/
  template = loader.get_template('analysis.html')
  
  # result_dict = handle_uploaded_file("/static/documents/edam_data.csv")
  # respond with template with context
  # return HttpResponse(template.render(request, "webtool_result.html", result_dict))
  return HttpResponse(template.render(request))


def load_data():
  directory = BASE_DIR + '/analysis'
  features = np.genfromtxt(directory + static('pacific_plant_data.csv'), delimiter=',')
  labels = np.genfromtxt(directory + static('pacific_plant_label.csv'))
  return clean_features(features, labels)

# examine missing data by samples
def explore_samples(data, threshold=5):
  count = 0
  rows = []
  for i in range(len(data)):
    missing_vals = np.sum(np.isnan(data[i]))
    if missing_vals > threshold:
      rows.append(i)
      count += 1
  print count
  return rows

# examine missing data by features
def explore_features(data, threshold=100):
  cols = []
  for i in range(data.shape[1]):
    missing_vals = np.sum(np.isnan(data[:, i]))
    if missing_vals > threshold:
      print i, missing_vals
      cols.append(i)
  return cols

# remove missing data (detrimental features and samples)
def clean_features(features, labels):
  # remove features missing in a lot of samples
  feature_threshold = [300, 250, 200, 150, 100]
  sample_threshold = [20, 15, 10, 5, 0]

  for f, s in zip(feature_threshold, sample_threshold):
    remove_cols = explore_features(features, f)
    features = np.delete(features, remove_cols, axis=1)
    print features.shape
    print '---'
    
    # remove samples missing data
    remove_rows = explore_samples(features, s)
    features = np.delete(features, remove_rows, axis=0)
    labels = np.delete(labels, remove_rows)
    print features.shape, labels.shape
    print '---'

  # TODO: efficiently remove NaNs while keeping as much data as possibles
  return features, labels
 

# split training and test data
def split_data(features, labels):
  train_features, test_features, train_labels, test_labels = sklearn.model_selection.train_test_split(features, labels, test_size = 0.2)
  return train_features, test_features, train_labels, test_labels

def get_accuracy(predictions, labels):
  return float(np.sum(predictions == labels))/len(labels)

# build RF model
def predict_rf(train_features, test_features, train_labels, test_labels):
  model = RandomForestClassifier(n_estimators=1000)
  model.fit(train_features, train_labels)
  predictions = model.predict(train_features)
  print get_accuracy(predictions, train_labels)
  predictions = model.predict(test_features)
  print get_accuracy(predictions, test_labels)
  return predictions

# build LR model
def predict_lr(train_features, test_features, train_labels, test_labels):
  model = LogisticRegression()
  model.fit(train_features, train_labels)
  predictions = model.predict(train_features)
  print get_accuracy(predictions, train_labels)
  predictions = model.predict(test_features)
  print get_accuracy(predictions, test_labels)
  return predictions

# plot confusion matrix
def get_confusion_matrix(labels, predictions, normalize=True):
  cm = np.array([[0, 0], [0, 0]])
  for l, p in zip(labels.astype(int), predictions.astype(int)):
    cm[l][p] += 1
  if normalize:
    cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]
  return np.round(cm, 2)
  # sklearn confusion matrix has encoding error
  # cm = confusion_matrix(labels, predictions)
  # print cm
  # if normalize:
  #   cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
  # return cm

# test PCA and RF feature importances
def get_feature_importance(features, labels):
  model = RandomForestClassifier(n_estimators=1000)
  model.fit(features, labels)
  return model.feature_importances_

def get_pca_variance(features):
  model = PCA(n_components=18)
  model.fit(features)
  return model.explained_variance_ratio_

def get_principal_components(features, n_features=18):
  model = PCA(n_components=n_features)
  model.fit(features.T)
  return model.components_.T


@api_view(['GET'])
def confusion_matrix(request):
  directory = BASE_DIR + '/analysis'
  f = open(directory + static('pacific_plant_split.pkl'), 'rb')
  train_features, test_features, train_labels, test_labels = cPickle.load(f)
  f = open(directory + static('pacific_plant_rf.pkl'), 'rb')
  model = cPickle.load(f)
  predictions = model.predict(test_features)
  cm = get_confusion_matrix(test_labels, predictions)
  return Response(cm)


@api_view(['GET'])
def feature_importance(request):
  directory = BASE_DIR + '/analysis'
  f = open(directory + static('pacific_plant_rf.pkl'), 'rb')
  model = cPickle.load(f)
  return Response(model.feature_importances_)
  
@api_view(['GET'])
def pca_variance(request):
  return Response('test')
  
