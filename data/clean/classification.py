import numpy as np
import itertools
import matplotlib.pyplot as plt
import sklearn
from mpl_toolkits.mplot3d import Axes3D
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix

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
 

# split training and test data
def split_data(features, labels):
  train_features, test_features, train_labels, test_labels = sklearn.model_selection.train_test_split(features, labels, test_size = 0.2)
  return train_features, test_features, train_labels, test_labels

def get_accuracy(predictions, labels):
  return float(np.sum(predictions == labels))/len(labels)

# plot confusion matrix
def plot_confusion_matrix(cm, title='Confusion Matrix', normalize=True):
  if normalize:
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
  plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
  plt.colorbar()
  plt.title(title, fontsize=20)
  plt.ylabel('True Label', fontsize=16)
  plt.xlabel('Predicted Label', fontsize=16)
  threshold = cm.max() / 2.
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, round(cm[i, j], 2), horizontalalignment="center", color="white" if cm[i, j] > threshold else "black")
  plt.xticks(np.arange(2), [0, 1])
  plt.yticks(np.arange(2), [0, 1])
  plt.show()
  # plt.savefig('figures/rf_test_cm.png')

# build RF model
def predict_rf(train_features, test_features, train_labels, test_labels):
  model = RandomForestClassifier(n_estimators=1000)
  model.fit(train_features, train_labels)
  predictions = model.predict(train_features)
  print get_accuracy(predictions, train_labels)
  predictions = model.predict(test_features)
  print get_accuracy(predictions, test_labels)
  
  # create confusion matrix of prediction results
  # cm = confusion_matrix(test_labels, predictions)
  # plot_confusion_matrix(cm, title='Normalized Confusion Matrix (Test Data)')


# build LR model
def predict_lr(train_features, test_features, train_labels, test_labels):
  model = LogisticRegression()
  model.fit(train_features, train_labels)
  predictions = model.predict(train_features)
  print get_accuracy(predictions, train_labels)
  predictions = model.predict(test_features)
  print get_accuracy(predictions, test_labels)


# Notes:
# RF training accuracy: ~86%
# RF test accuracy: ~73%
# LR training accuracy: ~77%
# LR test accuracy: ~77%
# RF is more overfit but potentially better prediction


# test PCA and RF feature importances
def get_feature_importance(features, labels):
  model = RandomForestClassifier(n_estimators=1000)
  model.fit(features, labels)
  plt.bar(range(18), model.feature_importances_)
  plt.title('Random Forest Feature Importance', fontsize=20)
  plt.xlabel('Feature Index', fontsize=16)
  plt.ylabel('Feature Importance', fontsize=16)
  plt.show()
  # plt.savefig('figures/rf_feature_importance.png')
  # plt.close()

  model = PCA(n_components=18)
  model.fit(features)
  plt.bar(range(18), model.explained_variance_ratio_)
  plt.title('PCA Explained Variance', fontsize=20)
  plt.xlabel('Feature Index', fontsize=16)
  plt.ylabel('Explained Variance', fontsize=16)
  plt.show()
  # plt.savefig('figures/pca_explained_variance.png')

# Notes:
# PCA: 3 combined features contain 50% of variance 
# RF: variance much more uniformly distributed

def get_best_features(features, labels, n_features=18):
  model = RandomForestClassifier(n_estimators=1000)
  model.fit(features, labels)

  d = np.append(features[:, model.feature_importances_.argsort()[-n_features:][::-1]], labels.reshape(962, 1), axis=1)
  print d.shape
  cm = np.corrcoef(d.T)
  plt.imshow(cm, interpolation='nearest')
  plt.title('Top Features Correlation with Invasiveness (5)', fontsize=20)
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, round(cm[i, j], 2), horizontalalignment="center", color="white")
  plt.colorbar()
  # plt.show()
  plt.savefig('figures/correlation_matrix.png')

  return features[:, model.feature_importances_.argsort()[-n_features:][::-1]]


def get_principal_components(features, n_features=18):
  model = PCA(n_components=n_features)
  model.fit(features.T)
  return model.components_.T


features = np.genfromtxt('data/pacific_plant_data.csv', delimiter=',')
labels = np.genfromtxt('data/pacific_plant_label.csv')
features, labels = clean_features(features, labels)
# features = get_principal_components(features, 3)
# features = get_best_features(features, labels, 5)

# np.savetxt('data/clustering_features.csv', features, delimiter=',', fmt='%i')
# np.savetxt('data/clustering_labels.csv', labels, fmt='%i')
# get_feature_importance(features, labels)

train_features, test_features, train_labels, test_labels = split_data(features, labels)
# predict_rf(train_features, test_features, train_labels, test_labels)
# predict_lr(train_features, test_features, train_labels, test_labels)


