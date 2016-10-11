import pandas as pd
import sklearn
import sklearn.metrics as metrics
import numpy as np
import scipy
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn import cluster
from sklearn.linear_model import LogisticRegression as LR
from sklearn.ensemble import RandomForestClassifier as RFC
import warnings

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

def load_data(fileName, dropFirstColumn = True):
	df = pd.read_csv(fileName)
	if dropFirstColumn:
		df = df.drop(df[[0]], axis = 1)
	return df.as_matrix()

def predictLR(X, y):
	col_mean = np.nanmean(X,axis=0)
	inds = np.where(np.isnan(X))
	X[inds]=np.take(col_mean,inds[1])
	lr = LR()

	X_train, X_test, y_train, y_test = chooseRandom(X, y)
	lr.fit(X_train, y_train)
	return lr.score(X_test, y_test)

def predictRF(X, y):
	col_mean = np.nanmean(X,axis=0)
	inds = np.where(np.isnan(X))
	X[inds]=np.take(col_mean,inds[1])
	RF = RFC(n_estimators = 100)

	X_train, X_test, y_train, y_test = chooseRandom(X, y)
	RF.fit(X_train, y_train)
	return RF.score(X_test, y_test)

def predictGBC(X, y):
	col_mean = np.nanmean(X,axis=0)
	inds = np.where(np.isnan(X))
	X[inds]=np.take(col_mean,inds[1])
	
	gbc = GBC(n_estimators = 100)

	X_train, X_test, y_train, y_test = chooseRandom(X, y)
	gbc.fit(X_train, y_train)
	return gbc.score(X_test, y_test)

def delete_unimportant(X, important):
	return np.delete(X, important, 1)

def feature_combination(X, imp, category):
	imp_len = len(imp)
	cat_len = len(category)

	newX = np.empty([X.shape[0], imp_len+cat_len-1])
	for i in range(len(category)-1):
		# print(category[i])
		nextX = X[:,category[i]:category[i+1]]
		# print(nextX.shape)
		newX[:,i] = np.nansum(nextX, axis=1)
		# print(newX.shape)
	for i in range(imp_len):
		newX[:,i+cat_len-1] = X[:,i]

	return newX

def sampleAndAverage(method, method_string, iterations, X, y):
	# print("[{}] start score calculation for {} iterations".format(method_string, iterations))
	score = 0
	for _ in range(iterations):
		col_mean = np.nanmean(X,axis=0)
		inds = np.where(np.isnan(X))
		X[inds]=np.take(col_mean,inds[1])
		score += method(X, y)
	print("[{}] average score: {}".format(method_string, score/iterations))

def chooseRandom(x, y):
	x_train, x_test, y_train, y_test = sklearn.cross_validation.train_test_split(x, y, test_size = 0.5)
	return x_train, x_test, y_train, y_test


sample_size = 100

# From ecological literature- maybe feature 15
important = [0, 3, 6, 7, 15, 27, 35, 36, 37, 38, 39, 40, 41, 44]
category = [0, 3, 8, 13, 25, 29, 36, 44, 49]

warnings.filterwarnings('ignore')

X = load_data("pier_html_data_noevaluates.csv")
y = np.ravel(load_data("pier_html_labels_noevaluates.csv", False))
p = np.random.permutation(X.shape[0])
X = X[p]
y = y[p]
col_mean = np.nanmean(X,axis=0)
inds = np.where(np.isnan(X))
X[inds]=np.take(col_mean,inds[1])
# X = SelectKBest(f_classif, k=15).fit_transform(X, y)

print("RUNNING ITERATION {} FOR AVERAGE SCORE".format(sample_size))
print("--------------PIER DATA SET LR-----------------")

sampleAndAverage(predictLR, "predictLR", sample_size, X, y)
sampleAndAverage(predictLR, "predictLR- important only", sample_size, delete_unimportant(X, important), y)
# sampleAndAverage(predictLR, "predictLR- important + avg", sample_size, feature_combination(X, important, category), y)

print("--------------PIER DATA SET RF-----------------")
sampleAndAverage(predictRF, "predictRF", sample_size, X, y)
sampleAndAverage(predictRF, "predictRF- important only", sample_size, delete_unimportant(X, important), y)
# sampleAndAverage(predictRF, "predictRF- important + avg", sample_size, feature_combination(X, important, category), y)

print("--------------PIER DATA SET GBC-----------------")
sampleAndAverage(predictGBC, "predictGBC", sample_size, X, y)
sampleAndAverage(predictGBC, "predictGBC- important only", sample_size, delete_unimportant(X, important), y)
# sampleAndAverage(predictGBC, "predictGBC- important + avg", sample_size, feature_combination(X, important, category), y)




# pred_labels_train = predict(model, X_train)
# pred_labels_test = predict(model, X_test)
# print("Closed form solution")
# print("Train accuracy: {0}".format(metrics.accuracy_score(labels_train, pred_labels_train)))
