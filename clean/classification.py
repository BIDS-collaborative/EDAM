import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA

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
  # remove features by threshold
  remove_cols = explore_features(features, 100)
  features = np.delete(features, remove_cols, axis=1)
  print features.shape
  print '---'
  
  # remove samples by threshold
  remove_rows = explore_samples(features, 0)
  features = np.delete(features, remove_rows, axis=0)
  labels = np.delete(labels, remove_rows)
  print features.shape, labels.shape
  print '---'

  # TODO: efficiently remove NaNs while keeping as much data as possibles
  return features, labels
 

# split training and test data
def split_data(features, labels):
  train_features, test_features, train_labels, test_labels = sklearn.cross_validation.train_test_split(features, labels, test_size = 0.2)
  return train_features, test_features, train_labels, test_labels

# build RF model
def predict_rf(train_features, test_features, train_labels, test_labels):
  model = RandomForestClassifier(n_estimators=100)
  model.fit(train_features, train_labels)
  print model.score(train_features, train_labels)
  print model.score(test_features, test_labels)

# build LR model
def predict_lr(train_features, test_features, train_labels, test_labels):
  model = LogisticRegression()
  model.fit(train_features, train_labels)
  print model.score(train_features, train_labels)
  print model.score(test_features, test_labels)

# Notes:
# RF training accuracy: ~86%
# RF test accuracy: ~73%
# LR training accuracy: ~77%
# LR test accuracy: ~77%
# RF is more overfit but potentially better prediction


# test PCA and RF feature importances
def get_feature_importance(features):
  model = PCA(n_components=18)
  model.fit(features)
  plt.bar(range(18), model.explained_variance_ratio_)
  plt.show()

  model = RandomForestClassifier(n_estimators=500)
  model.fit(features, labels)
  plt.bar(range(18), model.feature_importances_)
  plt.show()

# Notes:
# PCA: 3 features contain 50% of variance 
# RF: variance much more uniformly distributed



features = np.genfromtxt('pacific_plant_data.csv', delimiter=',')
labels = np.genfromtxt('pacific_plant_label.csv')
features, labels = clean_features(features, labels)
# get_feature_importance(features)
train_features, test_features, train_labels, test_labels = split_data(features, labels)
predict_rf(train_features, test_features, train_labels, test_labels)
predict_lr(train_features, test_features, train_labels, test_labels)