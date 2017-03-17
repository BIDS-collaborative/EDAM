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

from .forms import DocumentForm 
from .forms import HyperparameterForm

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
    hyper_form = HyperparameterForm()
    return render(request, 'webtool.html', {'DocumentForm': doc_form, 'HyperparameterForm': hyper_form})


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


# examine missing data by samples
def explore_samples(data, threshold=5):
  count = 0
  rows = []
  for i in range(len(data)):
    missing_vals = np.sum(np.isnan(data[i]))
    if missing_vals > threshold:
      rows.append(i)
      count += 1
  print(count)
  return rows

# examine missing data by features
def explore_features(data, threshold=100):
  cols = []
  for i in range(data.shape[1]):
    missing_vals = np.sum(np.isnan(data[:, i]))
    if missing_vals > threshold:
      print(i, missing_vals)
      cols.append(i)


def clean_features(features, labels):
  # remove features missing in a lot of samples
  feature_threshold = [300, 250, 200, 150, 100]
  sample_threshold = [20, 15, 10, 5, 0]

  for f, s in zip(feature_threshold, sample_threshold):
    remove_cols = explore_features(features, f)
    features = np.delete(features, remove_cols, axis=1)
    print(features.shape)
    
    # remove samples missing data
    remove_rows = explore_samples(features, s)
    features = np.delete(features, remove_rows, axis=0)
    labels = np.delete(labels, remove_rows)
    print(features.shape, labels.shape)

  # RATIONALE: any feature missing in more than 5% of 
  # samples has no guarantee of being collected so do
  # not include in model and any sample still missing
  # data probably is fairly unknown or poorly recorded

  # TODO: efficiently remove NaNs while keeping as much data as possibles
  return features, labels


def train_rf(train_features, train_labels):
    print("train_rf")
    model = RandomForestClassifier(n_estimators=1000)
    print("rf model get")
    print(np.shape(train_features), np.any(np.isnan(train_features)), np.all(np.isfinite(train_features)))
    print(np.shape(train_labels), np.any(np.isnan(train_labels)), np.all(np.isfinite(train_labels)))

    model.fit(train_features, train_labels)
    print("rf model fitted")
    return model
    
def train_lr(train_features, train_labels):
    print("train_lr")
    model = LogisticRegression()
    model.fit(train_features, train_labels)
    return model

def get_accuracy(predictions, labels):
    return float(np.sum(predictions == labels))/len(labels)


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

@api_view(['GET'])
def model_selection(request):
  model = request.query_params.get('model')
  hyperparameters = request.query_params.get('hyperparameters').split(',')
  filename = request.query_params.get('filename')
  print model
  print hyperparameters
  print filename

  return Response(' ')
