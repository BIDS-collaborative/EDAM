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
from sklearn.ensemble import GradientBoostingClassifier as GBC
import warnings
from mpl_toolkits.mplot3d import Axes3D
from sklearn.feature_selection import RFE
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn import decomposition
from sklearn.model_selection import train_test_split
import itertools

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

	X_train, X_test, y_train, y_test = chooseRandom(X, y, 250)
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


def delete_unimportant(X, important):
	return np.delete(X, important, 1)


def sampleAndAverage(method, method_string, iterations, X, y):
	# print("[{}] start score calculation for {} iterations".format(method_string, iterations))
	score = 0
	for _ in range(iterations):
		col_mean = np.nanmean(X,axis=0)
		inds = np.where(np.isnan(X))
		X[inds]=np.take(col_mean,inds[1])
		score += method(X, y)
	#print("[{}] average score: {}".format(method_string, score/iterations))
	return score/iterations * 100

def chooseRandom(data, labels, size):
	"""Chooses test data and sample data randomly from the data"""
	x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size = size)
	return x_train, x_test, y_train, y_test 

#Preprocessing. Choose which columns to drop 
def dropColumns(X, columns):
	XT = X.T
	XT = np.delete(XT, columns, 0)
	return XT.T 


def testColumns(): 
    testing_col = [0,1,2,3,4,5,6,7,8,9,10,11,12,30,31,32,33,34,35,36,37,38,39,40,41]
    optimal_list = [0]
    best_list = []
    for L in range(21, 22):
        for subset in itertools.combinations(testing_col, L):
            lst = list(subset)
            t = sampleAndAverage(predictLR, "predictLR", sample_size, (dropColumns(X, lst)), y)
            if max(optimal_list) < t:
            	optimal_list.append(t)
            	best_list = lst
            	print(subset)
            	print(t)
            
            
    print ("Highest Score: {}".format(max(optimal_list)))
    #print ("Inputted Columns to Drop: {}".format(test_col))
    print ("Dropped Columns: {}".format(best_list))

	


sample_size = 100

# From ecological literature- maybe feature 15
important = [0, 3, 6, 7, 15, 27, 35, 36, 37, 38, 39, 40, 41, 44]
category = [0, 3, 8, 13, 25, 29, 36, 44, 49]
dropLR = [7, 9, 10, 11, 15, 26, 29, 31, 37]
noDropLR = [8, 24, 35, 40, 41, 44]
# dropLR = [9, 10, 11, 26, 31]

warnings.filterwarnings('ignore')

# np.random.seed(3)
X = load_data("pier_html_data_noevaluates.csv")
y = np.ravel(load_data("pier_html_labels_noevaluates.csv", False))	
col_mean = np.nanmean(X,axis=0)
inds = np.where(np.isnan(X))
X[inds]=np.take(col_mean,inds[1])
t = sampleAndAverage(predictLR, "predictLR", sample_size, (dropColumns(X, [0, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 21, 25, 26, 27, 28, 29]
)), y)

testColumns()
#print(t)