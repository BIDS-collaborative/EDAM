import pandas as pd
import sklearn
import numpy as np
import warnings
from sklearn.cluster import KMeans

def load_data(fileName, dropFirstColumn = True):
	df = pd.read_csv(fileName)
	if dropFirstColumn:
		df = df.drop(df[[0]], axis = 1)
	return df.as_matrix()

def predictKMeans(X, y):
	col_mean = np.nanmean(X,axis=0)
	inds = np.where(np.isnan(X))
	X[inds]=np.take(col_mean,inds[1])
	km = KMeans(n_clusters=2)

	X_train, X_test, y_train, y_test = chooseRandom(X, y)
	km.fit(X_train, y_train)
	return km.score(X_test, y_test)

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
warnings.filterwarnings('ignore')


X = load_data("pier_ne_data.csv")
y = np.ravel(load_data("pier_ne_labels.csv", False))

print("RUNNING ITERATION {} FOR AVERAGE SCORE".format(sample_size))
print("--------------NE DATA SET KMEANS-----------------")

sampleAndAverage(predictKMeans, "predictKMeans", sample_size, X, y)
