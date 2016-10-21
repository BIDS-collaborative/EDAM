import pandas as pd
import sklearn
import sklearn.metrics as metrics
import numpy as np
import scipy
import matplotlib.pyplot as plt
import warnings
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression as LR
from sklearn.ensemble import RandomForestClassifier as RFC

def load_data(fileName, dropFirstColumn = True):
	df = pd.read_csv(fileName)
	if dropFirstColumn:
		df = df.drop(df[[0]], axis = 1)
	return df.as_matrix()

def predictLR(X, y):
	col_mean = np.nanmean(X,axis=0)
	inds = np.where(np.isnan(X))
	X[inds]=np.take(col_mean,inds[1])

	lr = LR(multi_class = "multinomial", solver = "newton-cg")
	lr.fit(X[:500],y[:500])
	return lr.score(X[500:], y[500:])

def predictRF(X, y):
	col_mean = np.nanmean(X,axis=0)
	inds = np.where(np.isnan(X))
	X[inds]=np.take(col_mean,inds[1])

	RF = RFC(n_estimators = 100)
	forest = RF.fit(X[:500], y[:500])
	return forest.score(X[500:], y[500:])

def selectFeatureByPercentage(X, threshold):
	removedList = list()
	for i in range(X.shape[1]):
		column = X[:,i]
		nan_count = np.count_nonzero(np.isnan(column))
		nan_percent = nan_count/float(X.shape[0])
		if nan_percent > threshold:
			removedList.append(i)
	return np.delete(X, removedList, 1)

def selectFeatureByNumber(X, threshold):
	removedList = list()
	for i in range(X.shape[1]):
		column = X[:,i]
		nan_count = np.count_nonzero(np.isnan(column))
		if nan_count > threshold:
			removedList.append(i)
	return np.delete(X, removedList, 1)

def combineFeatureByMean(X, category):
	newX = np.empty([X.shape[0],len(category)-1])
	for i in range(len(category)-1):
		# print(category[i])
		nextX = X[:,category[i]:category[i+1]]
		# print(nextX.shape)
		newX[:,i] = np.nanmean(nextX, axis=1)
		# print(newX.shape)
	return newX

def combineFeatureBySum(X, category):
	newX = np.empty([X.shape[0],len(category)-1])
	for i in range(len(category)-1):
		# print(category[i])
		nextX = X[:,category[i]:category[i+1]]
		# print(nextX.shape)
		newX[:,i] = np.nansum(nextX, axis=1)
		# print(newX.shape)
	return newX


def sampleAndAverage(method, method_string, iterations, X, y):
	# print("[{}] start score calculation for {} iterations".format(method_string, iterations))
	score = 0
	for _ in range(iterations):
		p = np.random.permutation(X.shape[0])
		X = X[p]
		y = y[p]
		col_mean = np.nanmean(X,axis=0)
		inds = np.where(np.isnan(X))
		X[inds]=np.take(col_mean,inds[1])
		score += method(X, y)
	print("[{}] average score: {}".format(method_string, score/iterations))





sample_size = 100
category = [0, 3, 8, 13, 25, 29, 36, 44, 49]
warnings.filterwarnings('ignore')

print("RUNNING ITERATION {} FOR AVERAGE SCORE".format(sample_size))
print()
print("--------------FULL DATA SET LR-----------------")

X = load_data("pier_full_data.csv")
y = np.ravel(load_data("pier_full_labels.csv", False))

sampleAndAverage(predictLR, "predictLR", sample_size, X, y)
sampleAndAverage(predictLR, "averageLR", sample_size, combineFeatureByMean(X, category), y)
sampleAndAverage(predictLR, "sumfeatLR", sample_size, combineFeatureBySum(X, category), y)
for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
	sampleAndAverage(predictLR, "LR-SBP{}".format(i), sample_size, selectFeatureByPercentage(X, i), y)
for i in [300, 400, 500, 600, 700, 800]:
	sampleAndAverage(predictLR, "LR-SBN{}".format(i), sample_size, selectFeatureByNumber(X, i), y)

print("--------------FULL DATA SET RF-----------------")

sampleAndAverage(predictRF, "predictRF", sample_size, X, y)
sampleAndAverage(predictRF, "averageRF", sample_size, combineFeatureByMean(X, category), y)
sampleAndAverage(predictRF, "sumfeatRF", sample_size, combineFeatureBySum(X, category), y)
for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
	sampleAndAverage(predictRF, "RF-SBP{}".format(i), sample_size, selectFeatureByPercentage(X, i), y)
for i in [300, 400, 500, 600, 700, 800]:
	sampleAndAverage(predictRF, "RF-SBN{}".format(i), sample_size, selectFeatureByNumber(X, i), y)

print("--------------NE DATA SET LR-----------------")

X = load_data("pier_ne_data.csv")
y = np.ravel(load_data("pier_ne_labels.csv", False))

sampleAndAverage(predictLR, "predictLR", sample_size, X, y)
sampleAndAverage(predictLR, "averageLR", sample_size, combineFeatureByMean(X, category), y)
sampleAndAverage(predictLR, "sumfeatLR", sample_size, combineFeatureBySum(X, category), y)
for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
	sampleAndAverage(predictLR, "LR-SBP{}".format(i), sample_size, selectFeatureByPercentage(X, i), y)
for i in [300, 400, 500, 600, 700, 800]:
	sampleAndAverage(predictLR, "LR-SBN{}".format(i), sample_size, selectFeatureByNumber(X, i), y)

print("--------------NE DATA SET RF-----------------")

sampleAndAverage(predictRF, "predictRF", sample_size, X, y)
sampleAndAverage(predictRF, "averageRF", sample_size, combineFeatureByMean(X, category), y)
sampleAndAverage(predictRF, "sumfeatRF", sample_size, combineFeatureBySum(X, category), y)
for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
	sampleAndAverage(predictRF, "RF-SBP{}".format(i), sample_size, selectFeatureByPercentage(X, i), y)
for i in [300, 400, 500, 600, 700, 800]:
	sampleAndAverage(predictRF, "RF-SBN{}".format(i), sample_size, selectFeatureByNumber(X, i), y)













