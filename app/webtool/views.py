import numpy as np
import pickle as cPickle
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

import sklearn
import itertools
import os
import json
from sklearn.decomposition import PCA

from .forms import DocumentForm 

def index(request):
  if request.method == 'POST':
    form = DocumentForm(request.POST, request.FILES)

    if form.is_valid():
      print("form received")
      form.save()
      training_info = handle_uploaded_file(form.cleaned_data['document'], form.cleaned_data['label'])
      return render(request, 'test2.html', training_info)

    print(form._errors)
    return render(request, 'test2.html', {"RF":None, "LR":None})
  else:
    doc_form = DocumentForm()
    return render(request, 'webtool.html', {'DocumentForm': doc_form})


def handle_uploaded_file(doc, label):
  features = np.genfromtxt(doc, delimiter=',',skip_header=True)
  labels = np.genfromtxt(label, delimiter=',',skip_header=True)

  # labels = data[1:,-1]
  # features = features[1:,:]

  labels[np.isnan(labels)] = 0
  labels[np.isfinite(labels)==False] = 0

  features[np.isnan(features)] = 0
  features[np.isfinite(features)==False] = 0

  print(np.shape(features), np.any(np.isnan(features)), np.all(np.isfinite(features)))

  rf_result = performClassification(features, labels, "RF", train=True)
  lr_result = performClassification(features, labels, "LR", train=True)

  result_dict = {"RF":rf_result, "LR":lr_result}
  return result_dict

def hyperparameter_uploads(request):
  if request.method == 'POST':
    form = HyperparameterForm(request.POST, request.FILES)

    if form.is_valid():
      print("hyperparameters received")
      form.save()
      submission_info = {"model_choice": form.cleaned_data['model_choice'], "hyperparameters": form.cleaned_data['hyperparameters'], "filename": form.cleaned_data['filename']}
      return render(request, 'test2.html', submission_info)
    else:
      print(form._errors)
      return render(request, 'test2.html', {"RF":None, "LR":None})
  else:
    doc_form = DocumentForm()
    hyper_form = HyperparameterForm()
    return render(request, 'webtool.html', {'DocumentForm': doc_form, 'HyperparameterForm': hyper_form})

#We can do 2 things with the data right now:
#1. Split the data into a training set and test set, training the data and then running prediction on the test set.
#2. Predict using a stored in model. Right now it's just the model trained by the dataset. 
#Returns the predictions, model, and confusion matrix

def split_data(features, labels):
  print("split_data")
  train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.2)
  return train_features, test_features, train_labels, test_labels




def performClassification(data_features, data_label, model_name, train = False):
  if train:
    train_features, test_features, train_labels, test_labels = split_data(data_features, data_label)
    if model_name == "LR":
      model = train_lr(train_features, train_labels)
      predictions = model.predict(test_features)
    elif model_name == "RF":
      model = train_rf(train_features,train_labels)
      predictions = model.predict(test_features)
    print("done prediction", np.shape(predictions))
  else:
    with open("model" + model_name + ".pkl", 'rb') as fid:
      model = cPickle.load(fid)
    predictions = model.predict(data_features)

  cm = None
  if data_label != None:
    cm = confusion_matrix(test_labels, predictions)
    print(cm)
  return (model_name, predictions, cm)



def load_data(data, labels):
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  directory =  BASE_DIR + "/documents/" 
  print directory
  print data
  features = np.genfromtxt(directory + data, delimiter=',')
  labels = np.genfromtxt(directory + labels, delimiter = ",")
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
  # cm = confusion_matrix(labels, predictions)
  # print cm
  # if normalize:
  #   cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
  # return cm

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

#confusion matrix, feature importance, model predictions, pca variance
@api_view(['GET'])
def model_selection(request):
  model = request.query_params.get('model')
  hyperparameters = request.query_params.get('hyperparameters').split(',')
  features = request.query_params.get('features')
  labels = request.query_params.get('labels')
  data = load_data(features, labels)
  train_features, test_features, train_labels, test_labels = split_data(data[0], data[1])
  if model == " LR":
    predictions = predict_lr(train_features, test_features, train_labels, test_labels)
  else:
    predictions = predict_rf(train_features, test_features, train_labels, test_labels)
  counts, cm = get_confusion_matrix(test_labels, predictions)
  tips = [str(counts[0][0]) + ' out of ' + str(counts[0][0] + counts[0][1]),
    str(counts[0][1]) + ' out of ' + str(counts[0][0] + counts[0][1]),
    str(counts[1][0]) + ' out of ' + str(counts[1][0] + counts[1][1]),
    str(counts[1][1]) + ' out of ' + str(counts[1][0] + counts[1][1])]
  fi = get_feature_importance(data[0], data[1])
  fi = fi.tolist()
  pca = get_pca_variance(data[0])


  princomps = get_principal_components(data[0], 2)
  feature1 = princomps[:,0]
  feature2  = princomps[:,1]
  species = [0]*len(princomps[:,0])
  return Response({"feature_importance": {"features": np.zeros(len(fi)).tolist(), "importance": fi}, "predictions": predictions, "confusion_matrix": {"matrix": cm.tolist(), "tips": tips}, "pca": {"feature1": feature1, "feature2": feature2, "species": species, "label": data[1]}})
  # return Response({"model": model, "hyperparameters": hyperparameters, "features": features, "labels": labels})
