import numpy as np
import _pickle as cPickle
from sklearn.metrics import confusion_matrix



from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template import loader

from forms import DocumentForm 

def index(request):

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            training_info = handle_uploaded_file(form.cleaned_data['document'])
            return render(request, 'webtool_result.html', training_info)
    else:
        form = DocumentForm()
	    return render(request, 'webtool.html', {
	        'form': form
	    })


def handle_uploaded_file(file_path):
	data = np.genfromtxt(file_path, delimiter=',')
	labels = data[:,-1]
	features = data[:,:-1]

	rf_result = performClassification(features, labels, "RF")
	lr_result = performClassification(features, labels, "LR")

	result_dict = {"RF":rf_result, "LR":lr_result}
	return result_dict

#We can do 2 things with the data right now:
#1. Split the data into a training set and test set, training the data and then running prediction on the test set.
#2. Predict using a stored in model. Right now it's just the model trained by the dataset. 
#Returns the predictions, model, and confusion matrix

def split_data(features, labels):
	train_features, test_features, train_labels, test_labels = sklearn.cross_validation.train_test_split(features, labels, test_size = 0.2)
	return train_features, test_features, train_labels, test_labels


def train_rf(train_features, train_labels):
	model = RandomForestClassifier(n_estimators=1000)
	model.fit(train_features, train_labels)
	return model
	
def train_lr(train_features, train_labels):
	model = LogisticRegression()
	model.fit(train_features, train_labels)
	return model

def get_accuracy(predictions, labels):
	return float(np.sum(predictions == labels))/len(labels)


def performClassification(data_features, data_label, model_name, train = False):
	if train:
		train_features, test_features, train_labels, test_labels = split_data(features, labels)
		if model_name == "LR":
			model = train_lr(train_features, test_features, train_labels, test_labels)
			predictions = predict_lr(train_features, test_features, train_labels, test_labels)
		elif model_name == "RF":
			model = train_rf(train_features, test_features, train_labels, test_labels)
		predictions = model.predict(data_features)

	else:
		with open("model" + model_name + ".pkl", 'rb') as fid:
			model = cPickle.load(fid)
		predictions = model.predict(data_features)
	cm = None
	if data_label != None:
		cm = confusion_matrix(data_labels, predictions)
	return (model_name, predictions, cm)