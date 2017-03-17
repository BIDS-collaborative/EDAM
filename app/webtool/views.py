import numpy as np
import pickle as cPickle
import json

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import Imputer

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.templatetags.static import static

from .forms import DocumentForm 

from rest_framework.response import Response
from rest_framework.decorators import api_view


def index(request):
  if request.method == 'POST':
    form = DocumentForm(request.POST, request.FILES)

    if form.is_valid():
      form.save()
      handle_uploaded_file(form.cleaned_data['document'], form.cleaned_data['label'])
      template = loader.get_template('webtool.html')
      return HttpResponse(template.render(request))

  else:
    form = DocumentForm()
    return render(request, 'webtool.html', {'form': form})



def handle_uploaded_file(doc, label):
  features = np.genfromtxt(doc, delimiter=',',skip_header=True)
  labels = np.genfromtxt(label, delimiter=',',skip_header=True)

  # temporary way to handle missing values, should be replaced
  labels[np.isnan(labels)] = 0
  labels[np.isfinite(labels)==False] = 0
  features[np.isnan(features)] = 0
  features[np.isfinite(features)==False] = 0

  rf_result = performClassification(features, labels, "RF", train=True)
  lr_result = performClassification(features, labels, "LR", train=True)

  result_dict = {"RF":rf_result, "LR":lr_result}

  with open(doc+"_data", 'w') as f:
    json.dump(result_dict, f)


@api_view(['GET'])
def return_all_data(request):
  data_file = request['GET'].get("document")
  with open(data_file+"_data", 'r') as f:
    data = f.read()
  return Response(data)



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
  dic = {"model":model_name, "prediction": predictions.tolist(), "matrix": cm.tolist()}
  return dic












