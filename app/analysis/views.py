"""
This module defines the application's views, which are needed to render pages.
"""
import os
import json

import numpy as np
from django.shortcuts import render
from django.templatetags.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

from analysis.models import PierData


def index(request):
    """
    renders the page with html
    """
    # template = loader.get_template('analysis.html')
    return render(request, 'analysis.html')


def load_data():
    """
    load PIER data from static documents
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = BASE_DIR + '/analysis'
    features = np.genfromtxt(directory + static('pacific_plant_data.csv'), delimiter=',')
    labels = np.genfromtxt(directory + static('pacific_plant_label.csv'))
    feature_names = np.genfromtxt(directory + static('pacific_plant_features.csv'), delimiter='\n',
                                  dtype=str)
    return clean_features(features, labels, feature_names)


def explore_samples(data, threshold=5):
    """
    examine missing data by samples
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


def explore_features(data, threshold=100):
    """
    examine missing data by features
    """
    cols = []
    for i in range(data.shape[1]):
        missing_vals = np.sum(np.isnan(data[:, i]))
        if missing_vals > threshold:
            print(i, missing_vals)
            cols.append(i)
    return cols

def clean_features(features, labels, feature_names):
    """
    remove missing data (detrimental features and samples)
    """
    # remove features missing in a lot of samples
    feature_threshold = [300, 250, 200, 150, 100]
    sample_threshold = [20, 15, 10, 5, 0]

    for f, s in zip(feature_threshold, sample_threshold):
        _cols = explore_features(features, f)
        features = np.delete(features, remove_cols, axis=1)
        feature_names = np.delete(feature_names, remove_cols)
        print(features.shape)
        print('---')

        # remove samples missing data
        remove_rows = explore_samples(features, s)
        features = np.delete(features, remove_rows, axis=0)
        labels = np.delete(labels, remove_rows)
        print(features.shape, labels.shape)
        print('---')

    # TODO: efficiently remove NaNs while keeping as much data as possibles
    return features, labels, feature_names


def split_data(features, labels):
    """
    split training and test data
    """
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels,
                                                                                test_size=0.2)
    return train_features, test_features, train_labels, test_labels


def get_accuracy(predictions, labels):
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
    """
    build LR model
    """
    model = LogisticRegression()
    model.fit(train_features, train_labels)
    predictions = model.predict(train_features)
    # print get_accuracy(predictions, train_labels)
    predictions = model.predict(test_features)
    # print get_accuracy(predictions, test_labels)
    return predictions


def get_confusion_matrix(labels, predictions):
    """
    plot confusion matrix
    """
    cm = np.array([[0, 0], [0, 0]])
    for l, p in zip(labels.astype(int), predictions.astype(int)):
        cm[l][p] += 1
    norm_cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]
    return np.round(norm_cm, 2), cm
    # sklearn confusion matrix has encoding error


def get_feature_importance(features, labels):
    """
    test PCA and RF feature importances
    """
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
    # return model.components_.T


###
# The following functions are APIs that return data to generate plots
# They allow for caching the plot data in the database and return
# dictionaries containing the information neecessary for each plot
###


@api_view(['GET'])
def confusion_matrix(request):
    """
    confusion matrix requires 2x2 matrix, tooltips, and labels
    """
    data = dict()
    if not PierData.objects.filter(name='confusion_matrix').exists() or \
       request.query_params.get('reset'):
        features, labels, feature_names = load_data()
        train_features, test_features, train_labels, test_labels = split_data(features, labels)
        predictions = predict_rf(train_features, test_features, train_labels, test_labels)
        cm, counts = get_confusion_matrix(test_labels, predictions)
        data['matrix'] = cm.tolist()
        data['tips'] = [str(counts[0][0]) + ' out of ' + str(counts[0][0] + counts[0][1]),
                        str(counts[0][1]) + ' out of ' + str(counts[0][0] + counts[0][1]),
                        str(counts[1][0]) + ' out of ' + str(counts[1][0] + counts[1][1]),
                        str(counts[1][1]) + ' out of ' + str(counts[1][0] + counts[1][1])]
        data['labels'] = ['Non-Invasive', 'Invasive']
        PierData.objects.update_or_create(name='confusion_matrix',
                                          defaults={'json': json.dumps(data)})
    else:
        data = json.loads(PierData.objects.get(name='confusion_matrix').json)

    return Response(data)


@api_view(['GET'])
def feature_importance(request):
    """
    feature importance requires a list of features and a list of importances
    """
    data = dict()
    if not PierData.objects.filter(name='feature_importance').exists() or \
       request.query_params.get('reset'):
        features, labels, feature_names = load_data()
        data['importance'] = get_feature_importance(features, labels).tolist()
        data['features'] = feature_names.tolist()
        PierData.objects.update_or_create(name='feature_importance',
                                          defaults={'json': json.dumps(data)}) 
    else:
        data = json.loads(PierData.objects.get(name='feature_importance').json)

    return Response(data)


@api_view(['GET'])
def pca_variance(request):
    """
    PCA variance requires a list of variances (this is not currently in use)
    """
    data = dict()
    if not PierData.objects.filter(name='pca_variance').exists() or \
       request.query_params.get('reset'):
        features, labels, feature_names = load_data()
        data['pca_variance'] = get_pca_variance(features)
        PierData.objects.create(name='pca_variance', json=json.dumps(data))
    else:
        data = json.loads(PierData.objects.get(name='pca_variance').json)

    return Response(data)


@api_view(['GET'])
def pca_scatter(request):
    """
    PCA scatter requires the values of 2 principal components and a list of labels (invasive or
    non-invasive) also takes in list of species as tooltips which is currently 0-filled
    """
    data = dict()
    if not PierData.objects.filter(name='pca_scatter').exists() or \
       request.query_params.get('reset'):
        features, labels, feature_names = load_data()
        princomps = get_principal_components(features, 2)
        data['feature1'] = princomps[:, 0].tolist()
        data['feature2'] = princomps[:, 1].tolist()
        data['species'] = [0] * len(princomps[:, 0])
        data['label'] = labels.tolist()
        PierData.objects.update_or_create(name='pca_scatter', defaults={'json': json.dumps(data)})
    else:
        data = json.loads(PierData.objects.get(name='pca_scatter').json)

    return Response(data)


@api_view(['GET'])
def pca_3d(request):
    """
    same as PCA scatter but with 3 principal components
    """
    data = dict()
    if not PierData.objects.filter(name='pca_3d').exists() or \
       request.query_params.get('reset'):
        features, labels, feature_names = load_data()
        princomps = get_principal_components(features, 3)
        data['feature1'] = princomps[:, 0].tolist()
        data['feature2'] = princomps[:, 1].tolist()
        data['feature3'] = princomps[:, 2].tolist()
        data['species'] = [0] * len(princomps[:, 0])
        data['label'] = labels.tolist()
        PierData.objects.update_or_create(name='pca_3d', defaults={'json': json.dumps(data)})
    else:
        data = json.loads(PierData.objects.get(name='pca_3d').json)

    return Response(data)
