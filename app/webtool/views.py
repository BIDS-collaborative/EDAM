"""
This module defines the application's views, which are needed to render pages and return page responses.

These views are split into two broad groups:
    * API endpoints, which dynamically send and receive data
    * Helper functions, which assist in cleaning, formatting, and analyzing data.

References:
    * Django Introduction to Views <https://docs.djangoproject.com/en/dev/topics/http/views/>
    * Scikit Learn Documentation <http://scikit-learn.org/stable/modules/classes.html>
    * Django REST Framework: <http://www.django-rest-framework.org/api-guide/views/>
"""
import os
import csv

import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render

from .forms import DocumentForm


def index(request):
    """
    Renders page with using HTML and includes Python objects as context

    This API endpoint responds differently depending on whether the request is a GET or POST. If the
    request is a GET, a DocumentForm object is included as context. If the request is a POST, the
    request's document and label fields are included as context.

    Args:
        request: The HTTP request object sent by the client.
    """
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'webtool.html', {'document': request.FILES['document'],
                                                    'label': request.FILES['label']})
    else:
        doc_form = DocumentForm()
        return render(request, 'webtool.html', {'DocumentForm': doc_form})


def load_data(document, labels, features_selected):
    """
    Prepares and returns cleaned data using the given document and labels. The document is sourced
    from the static `/documents/` directory.

    Args:
        document: The document being loaded from the `/documents/` directory.
        labels: The labels being loaded from the `/documents/` directory.
    Returns:
        Returns a cleaned set of features and labels, in a tuple. i.e. (<features>, <labels>)
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = BASE_DIR + "/documents/"
    print(directory)
    print(document)
    features = np.genfromtxt(directory + document, delimiter=',')
    labels = np.genfromtxt(directory + labels, delimiter=',')
    # feature_names = np.genfromtxt(directory + static('pacific_plant_features.csv'), delimiter='\n', dtype=str)
    feature_names = []
    with open(directory + document, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            feature_names.append(",".join(row))
    if features_selected:
        to_delete = []
        for i in range(len(feature_names)):
            if feature_names[i] not in features_selected:
                to_delete.append(i)
        features = np.delete(features, to_delete, axis=0)
    return clean_features(features, labels)


def remove_samples(data, threshold=5):
    """
    Aggregates the rows (species) in the data in which there are too many NaN (missing) values, as
    dictated by `threshold`.

    Args:
        data: The data object containing the species and their features.
        threshold: The limit to the number of NaN values a row can have.
    Returns:
        A list of rows with more than `threshold` amount of Nan values.
    """
    count = 0
    rows = []
    for i in enumerate(data):
        missing_vals = np.sum(np.isnan(data[i]))
        if missing_vals > threshold:
            rows.append(i)
            count += 1
    print(count)
    return rows


def remove_features(data, threshold=100):
    """
    Aggregates the columns (features) in the data in which there are too many NaN (missing) values, as
    dictated by `threshold`.

    Args:
        data: The data object containing the species and their features.
        threshold: The limit to the number of NaN values a column can have.
    Returns:
        A list of columns with more than `threshold` amount of Nan values.
    """
    cols = []
    for i in range(data.shape[1]):
        missing_vals = np.sum(np.isnan(data[:, i]))
        if missing_vals > threshold:
            print(i, missing_vals)
            cols.append(i)
    return cols


def clean_features(features, labels):
    """
    Remove missing and NaN values from the data.

    Args:
        features (numpy.array): An array of species features.
        labels (numpy.array): An array of species labels.

    Returns:
        The features and labels, with rows and columns with excessive NaN or missing values removed. 
    """
    # remove features missing in a lot of samples
    feature_threshold = [300, 250, 200, 150, 100]
    sample_threshold = [20, 15, 10, 5, 0]

    for f, s in zip(feature_threshold, sample_threshold):
        remove_cols = remove_features(features, f)
        features = np.delete(features, remove_cols, axis=1)
        # feature_names = np.delete(feature_names, remove_cols)
        print(features.shape)
        print('---')

        # remove samples missing data
        remove_rows = remove_samples(features, s)
        features = np.delete(features, remove_rows, axis=0)
        labels = np.delete(labels, remove_rows)
        print(features.shape, labels.shape)
        print('---')

    # TODO: efficiently remove NaNs while keeping as much data as possibles
    return features, labels

# TODO: Remove this redundant function. 
def split_data(features, labels):
    """
    Split the features and labels into training and test data. 
    """
    return train_test_split(features, labels, test_size=0.2)

def get_accuracy(predictions, labels):
    """
    Returns the accuracy of a given prediction.

    Args:

    Returns:
        
    """
    return float(np.sum(predictions == labels))/len(labels)


def predict_rf(train_features, test_features, train_labels, test_labels):
    """
    build RF model
    """
    model = RandomForestClassifier(n_estimators=1000)
    model.fit(train_features, train_labels)
    predictions = model.predict(train_features)
    # print get_accuracy(predictions, train_labels)
    predictions = model.predict(test_features)
    # print get_accuracy(predictions, test_labels)
    return predictions


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



@api_view(['GET'])
def model_selection(request):
    """
    An API endpoint that uses the Django REST framework to analyze the submitted data using the
    specified model and hyperparameters. Returns a REST response containing the metadata for the 
    analysis plots.

    Uses the Django REST framework's `api_view` decorator to make the function available as URL
    endpoint. When a user makes a request, the URL will have `/model_selection` in it, and `urls.py`
    will direct the request to this function.

    Args:
        request: The HTTP request object sent by the client.

    Returns:
        A Django REST Response object, constructed as a JSON object.
    """
    # get input parameters
    model = request.query_params.get('model')
    hyperparameters = request.query_params.get('hyperparameters').split(',')
    features = request.query_params.get('features')
    labels = request.query_params.get('labels')
    features_selected = request.query_params.get('features_selected')

    # load data files
    data = load_data(features, labels, features_selected)

    # train and test models
    train_features, test_features, train_labels, test_labels = split_data(data[0], data[1])
    if model == " LR":
        predictions = predict_lr(train_features, test_features, train_labels, test_labels)
    else:
        predictions = predict_rf(train_features, test_features, train_labels, test_labels)

    # create plot data
    confusion_matrix, counts = get_confusion_matrix(test_labels, predictions)
    tips = [str(counts[0][0]) + ' out of ' + str(counts[0][0] + counts[0][1]),
            str(counts[0][1]) + ' out of ' + str(counts[0][0] + counts[0][1]),
            str(counts[1][0]) + ' out of ' + str(counts[1][0] + counts[1][1]),
            str(counts[1][1]) + ' out of ' + str(counts[1][0] + counts[1][1])]
    feature_importance = get_feature_importance(data[0], data[1])
    feature_importance = feature_importance.tolist()
    pca_variance = get_pca_variance(data[0])
    principal_components = get_principal_components(data[0], 3)
    feature1 = principal_components[:, 0]
    feature2 = principal_components[:, 1]
    feature3 = principal_components[:, 2]
    species = [0]*len(principal_components[:, 0])
    return Response({"feature_importance": {"features": np.zeros(len(feature_importance)).tolist(),
                                            "importance": feature_importance},
                     "predictions": predictions,
                     "confusion_matrix": {"matrix": confusion_matrix.tolist(),
                                          "tips": tips,
                                          "labels": ['Non-Invasive', 'Invasive']},
                     "pca": {"feature1": feature1, "feature2": feature2, "species": species,
                             "label": data[1]},
                     "pca_3d": {"feature1": feature1, "feature2": feature2, "feature3": feature3,
                                "species": species, "label": data[1]},
                     "redirect": request.get_full_path()
                    })
