import numpy as np
import cPickle
from sklearn.metrics import confusion_matrix



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
			predictions = predict_lr(train_features, test_features, train_labels, test_labels)
		elif model == "RF":
			model = train_rf(train_features, test_features, train_labels, test_labels)
		predictions = model.predict(data_features)

	else:
		with open("model" + model + "pkl", 'rb') as fid:
			model = cPickle.load(fid)
		predictions = model.predict(data_features)
	cm = None
	if data_label != None:
		cm = confusion_matrix(data_labels, predictions)
	return (predictions, model, cm)