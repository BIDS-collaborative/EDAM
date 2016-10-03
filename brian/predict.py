import pandas as pd
import sklearn
import sklearn.metrics as metrics
import numpy as np
import scipy
import matplotlib.pyplot as plt
import  scipy.stats as stats
from sklearn import cluster
from sklearn.linear_model import LogisticRegression as LR
from sklearn.ensemble import RandomForestClassifier as RFC

def load_data(fileName, dropFirstColumn = True):
	df = pd.read_csv(fileName)
	if dropFirstColumn:
		df = df.drop(df[[0]], axis = 1)
	return df.as_matrix()

def predict(X, y):
	col_mean = stats.nanmean(X,axis=0)
	inds = np.where(np.isnan(X))
	X[inds]=np.take(col_mean,inds[1])

	k_means = cluster.KMeans(n_clusters = 6)
	k_means.fit(X, y)
	lr = LR(multi_class = "multinomial", solver = "newton-cg")
	lr.fit(X,y)
	return lr.score(X, y)


X = load_data("pier_html_data.csv")
y = np.ravel(load_data("pier_html_labels.csv", False))
col_mean = stats.nanmean(X,axis=0)
inds = np.where(np.isnan(X))
X[inds]=np.take(col_mean,inds[1])
score = predict(X, y)
# pred_labels_train = predict(model, X_train)
# pred_labels_test = predict(model, X_test)
# print("Closed form solution")
# print("Train accuracy: {0}".format(metrics.accuracy_score(labels_train, pred_labels_train)))
