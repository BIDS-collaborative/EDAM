import numpy as np
import cPickle
import sklearn
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template import loader

def index(request):
	# load html from templates/
	template = loader.get_template('webtool.html')
	context = {

	}
	# respond with template with context
	return HttpResponse(template.render(context, request))




def uploadData(request):
	return


def parseData(request):
	return

#We can do 2 things with the data right now:
#1. Split the data into a training set and test set, training the data and then running prediction on the test set.
#2. Predict using a stored in model. Right now it's just the model trained by the dataset. 
#Returns the predictions, model, and confusion matrix

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

# Some statistics:
# total 1427 plants
# 1425 missing at least one feature
# 632 (44%) missing more than 10 features
# 196 (14%) missing more than 15 features
# only 22 (2%) missing more than 20 features
# all features missing in at least one sample

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

  # RATIONALE: any feature missing in more than 5% of 
  # samples has no guarantee of being collected so do
  # not include in model and any sample still missing
  # data probably is fairly unknown or poorly recorded

  # TODO: efficiently remove NaNs while keeping as much data as possibles
  return features, labels



def split_data(features, labels):
	train_features, test_features, train_labels, test_labels = sklearn.cross_validation.train_test_split(features, labels, test_size = 0.2)
	return train_features, test_features, train_labels, test_labels


def train_rf(train_features, test_features, train_labels, test_labels):
	model = RandomForestClassifier(n_estimators=1000)
	model.fit(train_features, train_labels)
	return model
	
def train_lr(train_features, test_features, train_labels, test_labels):
	model = LogisticRegression()
	model.fit(train_features, train_labels)
	return model

def get_accuracy(predictions, labels):
	return float(np.sum(predictions == labels))/len(labels)


def performClassification(data_features, data_label, model, train = False):

	if train:
		train_features, test_features, train_labels, test_labels = split_data(features, labels)
		if model == "LR":
			model = train_lr(train_features, test_features, train_labels, test_labels)
		elif model == "RF":
			model = train_rf(train_features, test_features, train_labels, test_labels)
		predictions = model.predict(data_features)

	else:
		with open("../static/webtool/model" + model + ".pkl", 'rb') as fid:
			model = cPickle.load(fid)
		predictions = model.predict(data_features)
	cm = None
	if data_label is not None:
		cm = confusion_matrix(data_label, predictions)
	return (predictions, model, cm)


# features = np.genfromtxt('../static/webtool/pacific_plant_data.csv', delimiter=',')
# labels = np.genfromtxt('../static/webtool//pacific_plant_label.csv')
# # features = np.delete(features, 0, 1)
# features, labels = clean_features(features, labels)
# c = performClassification(features, labels, "LR")
