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

from sklearn.feature_selection import RFE
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn import decomposition


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
	return score/iterations * 100

def chooseRandom(x, y):
	x_train, x_test, y_train, y_test = sklearn.cross_validation.train_test_split(x, y, test_size = 0.5)
	return x_train, x_test, y_train, y_test

#Preprocessing. Choose which columns to drop 
def dropColumns(X, columns):
	XT = X.T
	XT = np.delete(XT, columns, 0)
	return XT.T 

#Drop each column and make bar graph that shows performance after dropping the column
def compareFeatures(X, y):
	np.random.seed(1)
	LRscores = [sampleAndAverage(predictLR, "predictLR", 100, X, y)]
	# RFscores = [sampleAndAverage(predictRF, 50, X, y)]
	# GBCscores = [sampleAndAverage(predictGBC, "predictGBC", 50, X, y)]
	x = np.arange(X.shape[1] + 1)
	for i in range(X.shape[1]):
		print i 
		newX = dropColumns(X, i)
		LRscore = sampleAndAverage(predictLR, "predictLR", 100, newX, y)
		# RFscore = sampleAndAverage(predictRF, 50, newX, y)
		# GBCscore = sampleAndAverage(predictGBC, "predictGBC", 50, newX, y)
		LRscores.append(LRscore)
		# RFscores.append(RFscore)
		# GBCscores.append(GBCscore)
	fig, ax = plt.subplots()
	width = 0.5
	ax.set_ylabel('Scores')
	ax.set_title('Scores with feature i deleted')
	ax.set_xticks(x + 0.5 * width)
	ax.set_xticklabels((x - 1))
	rects1 = ax.bar(x, LRscores, width, color='r')

	def autolabel(rects):
    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., height,
	                '%.2f' % height,
	                ha='center', va='bottom', fontsize = 7.5)

	autolabel(rects1)
	# rects2 = ax.bar(x + width, GBCscores, width, color='y')
	plt.show()
	return LRscores

#Preprocessing. Standarize the columns. Seems to make it worse.
def standardize(X, column = True):
    newMatrix = []
    if column:
        for i in range(X.shape[1]):
            mu = np.mean(np.transpose(X)[i])
            sigma = np.std(np.transpose(X)[i])
            newMatrix.append(np.array((np.transpose(X)[i] - mu) / sigma))
        newMatrix = np.array(newMatrix)
        newMatrix = np.transpose(newMatrix)

    else: 
        for i in range(X.shape[0]):
            mu = np.mean(X[i])
            sigma = np.std(X[i])
            newMatrix.append(np.array((X[i] - mu) / sigma))
        newMatrix = np.array(newMatrix)

    return newMatrix

#Preprocessing. Binarize the columns. Seems to make it worse
def binarize(X):
    newMatrix = []
    for i in range(X.shape[0]):
        row = []
        for j in range(X.shape[1]):
            if X[i][j] > 0:
                row.append(1)
            else:
                row.append(0)
        newMatrix.append(np.array(row))
    return np.array(newMatrix)


def pca_decomposition(X):
	pca = decomposition.PCA(n_components = 3)
	pca.fit(X)
	transformX = pca.transform(X)
	return transformX

def feature_selection(X, y):
	model = LR()
	rfe = RFE(model, 34)
	fit = rfe.fit(X, y)
	print("Num Features: %d") % fit.n_features_
	print("Selected Features: %s") % fit.support_
	print("Feature Ranking: %s") % fit.ranking_
	print fit.score(X, y)
	return fit.transform(X)
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
sampleAndAverage(predictRF, "predictRF", sample_size, pca_decomposition(feature_selection(X, y)), y)



# compareFeatures(dropColumns(X,dropLR), y)
# score1 = 0
# score2 = 0
# for i in range(100):
# 	p = np.random.permutation(X.shape[0])
# 	X = X[p]
# 	y = y[p]
# 	#Without dropping any columnsm, around 92.08% accuracy with LR
# 	XLR = dropColumns(X, dropLR)   #Around 92.3%
# 	# XLR = dropColumns(X, noDropLR)  #Around 85.6%

# 	score1 += sampleAndAverage(predictLR, "predictLR", sample_size, X, y)
# 	score2 += sampleAndAverage(predictLR, "predictLR drop", sample_size, XLR, y)
# print score1/100
# print score2/100

# X = SelectKBest(f_classif, k=15).fit_transform(X, y)

# print("RUNNING ITERATION {} FOR AVERAGE SCORE".format(sample_size))
# print("--------------PIER DATA SET LR-----------------")

# sampleAndAverage(predictLR, "predictLR", sample_size, X, y)
# sampleAndAverage(predictLR, "predictLR- important only", sample_size, delete_unimportant(X, important), y)
# sampleAndAverage(predictLR, "predictLR- important + avg", sample_size, feature_combination(X, important, category), y)

# print("--------------PIER DATA SET RF-----------------")
# sampleAndAverage(predictRF, "predictRF", sample_size, X, y)
# sampleAndAverage(predictRF, "predictRF- important only", sample_size, delete_unimportant(X, important), y)
# sampleAndAverage(predictRF, "predictRF- important + avg", sample_size, feature_combination(X, important, category), y)

# print("--------------PIER DATA SET GBC-----------------")
# sampleAndAverage(predictGBC, "predictGBC", sample_size, X, y)
# sampleAndAverage(predictGBC, "predictGBC- important only", sample_size, delete_unimportant(X, important), y)
# sampleAndAverage(predictGBC, "predictGBC- important + avg", sample_size, feature_combination(X, important, category), y)




# pred_labels_train = predict(model, X_train)
# pred_labels_test = predict(model, X_test)
# print("Closed form solution")
# print("Train accuracy: {0}".format(metrics.accuracy_score(labels_train, pred_labels_train)))