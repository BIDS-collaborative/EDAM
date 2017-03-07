from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.templatetags.static import static

from .models import PierData

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import numpy as np
import itertools
import sklearn
import os
import cPickle
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix


def index(request):
  template = loader.get_template('analysis.html')
  return HttpResponse(template.render(request))

def load_data():
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  directory = BASE_DIR + '/analysis'
  features = np.genfromtxt(directory + static('pacific_plant_data.csv'), delimiter=',')
  labels = np.genfromtxt(directory + static('pacific_plant_label.csv'))
  feature_names = np.genfromtxt(directory + static('pacific_plant_features.csv'), delimiter='\n', dtype=str)
  return clean_features(features, labels, feature_names)

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
def clean_features(features, labels, feature_names):
  # remove features missing in a lot of samples
  feature_threshold = [300, 250, 200, 150, 100]
  sample_threshold = [20, 15, 10, 5, 0]

  for f, s in zip(feature_threshold, sample_threshold):
    remove_cols = explore_features(features, f)
    features = np.delete(features, remove_cols, axis=1)
    feature_names = np.delete(feature_names, remove_cols)
    print features.shape
    print '---'
    
    # remove samples missing data
    remove_rows = explore_samples(features, s)
    features = np.delete(features, remove_rows, axis=0)
    labels = np.delete(labels, remove_rows)
    print features.shape, labels.shape
    print '---'

  # TODO: efficiently remove NaNs while keeping as much data as possibles
  return features, labels, feature_names

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
  # print get_accuracy(predictions, train_labels)
  predictions = model.predict(test_features)
  # print get_accuracy(predictions, test_labels)
  return predictions

# build LR model
def predict_lr(train_features, test_features, train_labels, test_labels):
  model = LogisticRegression()
  model.fit(train_features, train_labels)
  predictions = model.predict(train_features)
  # print get_accuracy(predictions, train_labels)
  predictions = model.predict(test_features)
  # print get_accuracy(predictions, test_labels)
  return predictions

# plot confusion matrix
def get_confusion_matrix(labels, predictions):
  cm = np.array([[0, 0], [0, 0]])
  for l, p in zip(labels.astype(int), predictions.astype(int)):
    cm[l][p] += 1
  norm_cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]
  return np.round(norm_cm, 2), cm
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

# cache PIER analysis data in database
# allow options for confusion matrix (training or test, prediction model)
@api_view(['GET'])
def confusion_matrix(request):
  data = dict()
  if (not PierData.objects.filter(name='confusion_matrix').exists()) or (request.query_params.get('reset')):
    features, labels, feature_names = load_data()
    train_features, test_features, train_labels, test_labels = split_data(features, labels)
    predictions = predict_rf(train_features, test_features, train_labels, test_labels)
    cm, counts = get_confusion_matrix(test_labels, predictions)
    data['matrix'] = cm.tolist()
    data['tips'] = [str(counts[0][0]) + ' out of ' + str(counts[0][0] + counts[0][1]), 
    str(counts[0][1]) + ' out of ' + str(counts[0][0] + counts[0][1]),
    str(counts[1][0]) + ' out of ' + str(counts[1][0] + counts[1][1]), 
    str(counts[1][1]) + ' out of ' + str(counts[1][0] + counts[1][1])]
    data['labels'] = ['Invasive', 'Non-Invasive']
    PierData.objects.update_or_create(name='confusion_matrix', defaults={'json': json.dumps(data)})
  else:
    data = json.loads(PierData.objects.get(name='confusion_matrix').json)
    
  return Response(data)


@api_view(['GET'])
def feature_importance(request):
  data = dict()
  if (not PierData.objects.filter(name='feature_importance').exists()) or (request.query_params.get('reset')):
    features, labels, feature_names = load_data()
    data['importance'] = get_feature_importance(features, labels).tolist()
    data['features'] = feature_names.tolist()
    PierData.objects.update_or_create(name='feature_importance', defaults={'json': json.dumps(data)})
  else:
    data = json.loads(PierData.objects.get(name='feature_importance').json)
    
  return Response(data)
  
@api_view(['GET'])
def pca_variance(request):
  pca_variance = None
  if PierData.objects.filter(name='pca_variance').exists():
    pca_variance = json.loads(PierData.objects.get(name='pca_variance').json)
  else:
    features, labels, feature_names = load_data()
    pca_variance = get_pca_variance(features)
    PierData.objects.create(name='pca_variance', json=json.dumps(pca_variance))
  return Response(pca_variance)
  
