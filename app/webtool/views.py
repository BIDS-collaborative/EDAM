import numpy as np
import pickle as cPickle
import json

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import Imputer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.templatetags.static import static

import sklearn
import itertools
import os
import json
from sklearn.decomposition import PCA

from .forms import DocumentForm

from rest_framework.response import Response
from rest_framework.decorators import api_view

# renders page with HTML and document form
# if form is submitted replace document form with uploaded files
def index(request):
  if request.method == 'POST':
    form = DocumentForm(request.POST, request.FILES)
    
    if form.is_valid():
      form.save()
      template = loader.get_template('webtool.html')
      return HttpResponse(template.render({'document': request.FILES['document'], 'label': request.FILES['label']}))

  else:
    doc_form = DocumentForm()
    return render(request, 'webtool.html', {'DocumentForm': doc_form})

# load data from static documents directory
def load_data(data, labels):
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  directory =  BASE_DIR + "/documents/"
  print (directory)
  print (data)
  features = np.genfromtxt(directory + data, delimiter=',')
  labels = np.genfromtxt(directory + labels, delimiter = ',')
  # feature_names = np.genfromtxt(directory + static('pacific_plant_features.csv'), delimiter='\n', dtype=str)
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
  print (count)
  return rows

# examine missing data by features
def explore_features(data, threshold=100):
  cols = []
  for i in range(data.shape[1]):
    missing_vals = np.sum(np.isnan(data[:, i]))
    if missing_vals > threshold:
      print (i, missing_vals)
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
    # feature_names = np.delete(feature_names, remove_cols)
    print (features.shape)
    print ('---')

    # remove samples missing data
    remove_rows = explore_samples(features, s)
    features = np.delete(features, remove_rows, axis=0)
    labels = np.delete(labels, remove_rows)
    print (features.shape, labels.shape)
    print ('---')

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

def get_confusion_matrix(labels, predictions):
  cm = np.array([[0, 0], [0, 0]])
  for l, p in zip(labels.astype(int), predictions.astype(int)):
    cm[l][p] += 1
  norm_cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]
  return np.round(norm_cm, 2), cm
  # sklearn confusion matrix has encoding error

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
  model.fit(features)
  return model.transform(features)


# web api that returns data for all analysis plots
# confusion matrix, feature importance, model predictions, pca variance
@api_view(['GET'])
def model_selection(request):
  # get input parameters
  model = request.query_params.get('model')
  hyperparameters = request.query_params.get('hyperparameters').split(',')
  features = request.query_params.get('features')
  labels = request.query_params.get('labels')

  # load data files
  data = load_data(features, labels)

  # train and test models
  train_features, test_features, train_labels, test_labels = split_data(data[0], data[1])
  if model == " LR":
    predictions = predict_lr(train_features, test_features, train_labels, test_labels)
  else:
    predictions = predict_rf(train_features, test_features, train_labels, test_labels)

  # create plot data
  cm, counts = get_confusion_matrix(test_labels, predictions)
  tips = [str(counts[0][0]) + ' out of ' + str(counts[0][0] + counts[0][1]),
    str(counts[0][1]) + ' out of ' + str(counts[0][0] + counts[0][1]),
    str(counts[1][0]) + ' out of ' + str(counts[1][0] + counts[1][1]),
    str(counts[1][1]) + ' out of ' + str(counts[1][0] + counts[1][1])]
  fi = get_feature_importance(data[0], data[1])
  fi = fi.tolist()
  pca = get_pca_variance(data[0])
  princomps = get_principal_components(data[0], 3)
  feature1 = princomps[:,0]
  feature2  = princomps[:,1]
  feature3  = princomps[:,2]
  species = [0]*len(princomps[:,0])
  return Response({"feature_importance": {"features": np.zeros(len(fi)).tolist(), "importance": fi},
    "predictions": predictions, 
    "confusion_matrix": {"matrix": cm.tolist(), "tips": tips, 'labels': ['Non-Invasive', 'Invasive']}, 
    "pca": {"feature1": feature1, "feature2": feature2, "species": species, "label": data[1]},
    "pca_3d": {"feature1": feature1, "feature2": feature2, "feature3": feature3, "species": species, "label": data[1]},
    "redirect": request.get_full_path()
  })
