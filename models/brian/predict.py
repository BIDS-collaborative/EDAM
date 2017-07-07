import pandas as pd
import sklearn
import sklearn.metrics as metrics
import numpy as np
import scipy
import matplotlib 

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
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.manifold import LocallyLinearEmbedding
from sklearn.manifold import Isomap
import sklearn.preprocessing as preprocessing
from pylab import pcolor, show, colorbar, xticks, yticks



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
	# print float(np.sum(lr.predict(X_test))) / float(X_test.shape[0])
	return lr.score(X_test, y_test)

def predictRF(X, y):
	col_mean = np.nanmean(X,axis=0)
	inds = np.where(np.isnan(X))
	X[inds]=np.take(col_mean,inds[1])
	RF = RFC(n_estimators = 100, criterion = "entropy")

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
	x_train, x_test, y_train, y_test = sklearn.cross_validation.train_test_split(x, y, test_size = 0.2)
	return x_train, x_test, y_train, y_test

def keepColumns(X, columns):
	XT = X.T
	XT = XT[columns]
	return XT.T

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


def pca_decomposition(X, y):
	pca = decomposition.PCA(n_components = 1)
	pca.fit(X)
	transformX = pca.transform(X)
	# print np.argmax(np.abs(pca.components_), axis = 1)
	plt.plot(pca.explained_variance_ratio_)
	# plt.show()
	# fig = plt.figure(1, figsize=(4, 3))
	# plt.clf()
	# ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
	# plt.cla()



	# ax.scatter(transformX[:, 0], transformX[:, 1], transformX[:, 2], c=y, cmap=plt.cm.spectral)

	# ax.w_xaxis.set_ticklabels([])
	# ax.w_yaxis.set_ticklabels([])
	# ax.w_zaxis.set_ticklabels([])



	# plt.show()


	return transformX


def localLinearEmbedding(X, y):
	lle = LocallyLinearEmbedding(n_components = 1, eigen_solver = "dense")
	lle.fit(X)
	transformX = lle.transform(X)
	return transformX

def isoMap(X, y):
	im = Isomap(n_components = 1, eigen_solver = "dense", n_neighbors = 20)
	im.fit(X)
	transformX = im.transform(X)
	return transformX

def feature_selection(X, y):
	model = LR()
	rfe = RFE(model, 10)
	fit = rfe.fit(X, y)
	print("Num Features: %d") % fit.n_features_
	print("Selected Features: %s") % fit.support_
	print("Feature Ranking: %s") % fit.ranking_
	print fit.score(X, y)
	return fit.transform(X)

def RF_feature_importance(X, y):
	forest = ExtraTreesClassifier(n_estimators=250, random_state=0)
	forest.fit(X, y)
	importances = forest.feature_importances_
	indices = np.argsort(importances)[::-1]
	print("Feature ranking:")
	for f in range(X.shape[1]):
		print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
	font = {'family' : 'normal',
	        'weight' : 'bold',
	        'size'   : 22}

	matplotlib.rc('font', **font)
	matplotlib.rcParams.update({'font.size': 15})

	plt.figure()
	plt.bar(range(X.shape[1]), importances[indices],
	       color="r", align="center")
	plt.xticks(range(X.shape[1]), indices)
	plt.xlim([-1, X.shape[1]])
	plt.show()


sample_size = 100

# # From ecological literature- maybe feature 15
# important = [0, 3, 6, 7, 15, 27, 35, 36, 37, 38, 39, 40, 41, 44]
# category = [0, 3, 8, 13, 25, 29, 36, 44, 49]
# dropLR = [7, 9, 10, 11, 15, 26, 29, 31, 37]
# noDropLR = [8, 24, 35, 40, 41, 44]
# # dropLR = [9, 10, 11, 26, 31]

# warnings.filterwarnings('ignore')

# np.random.seed(3)
X = load_data("pier_ne_data.csv")
y = np.ravel(load_data("pier_ne_labels.csv", False))
y_new = np.ravel(load_data("pier_ne_labels_new.csv", False))
# print y_new.shape
# print np.sum(y_new)

tooManyNans = []
for i in range(X.shape[1]):
	count = np.sum(np.isnan(X.T[i]))
	if float(count) / float(X.shape[0]) > 0.15:
		tooManyNans.append(i)
# #1, 2, 3, 5, 8, 12, 13, 14, 15, 16, 18, 20, 21, 22, 26, 29, 31, 32, 35, 37, 38, 40, 41, 43, 44, 45, 46, 47, 48

# # X2 = dropColumns(X, tooManyNans + [8, 1])

	
col_mean = np.nanmean(X,axis=0)
inds = np.where(np.isnan(X))
X[inds]=np.take(col_mean,inds[1])
# X = dropColumns(X, [8, 1])

# RF_feature_importance(X, y_new)

# Xtransform1 = keepColumns(X, [17, 20, 22, 24, 36]) #5 most important
# Xtransform2 = keepColumns(X, [17, 20, 22, 24, 36, 44, 40, 34, 32, 5]) #10 most important
# Xtransform3 = keepColumns(X, [17, 20, 22, 24, 36, 44, 40, 34, 32, 5, 18, 19, 21, 41, 46, 35, 47, 13, 19, 21]) #15 most important


# generalist = keepColumns(X, [22, 5])
# noninvasivethreats = keepColumns(X, [17, 20])
# other = keepColumns(X, [24, 36, 44, 40, 44, 32])

# x1 = pca_decomposition(generalist, y)
# x2 = pca_decomposition(noninvasivethreats, y)
# x3 = pca_decomposition(other, y)
# Xtransform4 = np.column_stack((x1, x2, x3))

# x4 = isoMap(generalist, y)
# x5 = isoMap(noninvasivethreats, y)
# x6 = isoMap(other, y)
# Xtransform5 = np.column_stack((x4, x5, x6))

#Old labels 

# RF_feature_importance(X, y)
# sampleAndAverage(predictLR, "predictLR", sample_size, X, y)
# sampleAndAverage(predictLR, "predictLR", sample_size, Xtransform1, y) #0.7808 for old labels
# sampleAndAverage(predictLR, "predictLR", sample_size, Xtransform2, y) #0.826 for old labels
# sampleAndAverage(predictLR, "predictLR", sample_size, Xtransform3, y) #0.787 for old labels
# # sampleAndAverage(predictLR, "predictLR", sample_size, Xtransform4, y_new)  #0.786 for old labels
# sampleAndAverage(predictLR, "predictLR", sample_size, Xtransform6, y)  #0.786 for old labels


# sampleAndAverage(predictLR, "predictLR", sample_size,Xtransform5, y)


# sampleAndAverage(predictLR, "predictLR", sample_size, feature_selection(X, y), y)
# sampleAndAverage(predictLR, "predictLR", sample_size, pca_decomposition(X, y), y)
#features 35, 7, 41, 34 
# sampleAndAverage(predictLR, "predictLR", sample_size, pca_decomposition(feature_selection(X, y), y), y)



#### NEW LABELS


# tooManyNans = []
# for i in range(X.shape[1]):
# 	count = np.sum(np.isnan(X.T[i]))
# 	if float(count) / float(X.shape[0]) > 0.10:
# 		tooManyNans.append(i)
#1, 2, 3, 5, 8, 12, 13, 14, 15, 16, 18, 20, 21, 22, 26, 29, 31, 32, 35, 37, 38, 40, 41, 43, 44, 45, 46, 47, 48


# X2 = dropColumns(X, [1, 2, 3, 5, 8, 12, 13, 14, 15, 16, 18, 20, 21, 22, 26, 29, 31, 32, 35, 37, 38, 40, 41, 43, 44, 45, 46, 47, 48])



# Xtransform6 = keepColumns(X, [46, 32, 34, 21, 35, 5, 47, 40, 22, 24, 41, 44, 16, 39, 20, 7, 18, 45, 14, 43]) #new labels feature rank. Got them from RF_feature_importance

# sampleAndAverage(predictLR, "predictLR new y", sample_size, Xtransform6, y_new)

# sampleAndAverage(predictRF, "predictRF new y", sample_size, Xtransform6, y_new)
# sampleAndAverage(predictLR, "predictLR keeping 15 most important features from before, new y", sample_size, Xtransform3, y_new)
# sampleAndAverage(predictLR, "predictLR keeping 10 most important features from before, new y", sample_size, Xtransform2, y_new)
# sampleAndAverage(predictRF, "predictRF keeping 10 most new important features, new y", sample_size, Xtransform6, y_new)
# sampleAndAverage(predictLR, "predictLR keeping 10 most new important features, new y", sample_size, Xtransform6, y_new)

# print float(np.sum(y_new)) / y_new.shape[0]
#Seeing which questions are left

# indices_left = set()
# for i in range(X.shape[1]):
# 	indices_left.add(i)
# for i in tooManyNans:
# 	indices_left.remove(i)
# # indices_left.remove(1)
# indices_left.remove(8)
# print tooManyNans
# print sorted(indices_left)[12]
# print sorted(indices_left)[19]
# print sorted(indices_left)[9]
# print sorted(indices_left)[10]


# X2 = dropColumns(X, tooManyNans + [1, 8])
RF_feature_importance(X, y_new) #new feature 44 most important 
# X2_transform = keepColumns(X2, [44, 30])

#Used 24 instead of 34 since did not change accuracy much for RF but it performs better for LR. Note that only keeping column 8 and 46 resulted in best accuracy of around 70%,
#while keeping column 32 and 24 resulted in ~69.4%
X3 = keepColumns(X, [8, 46, 32, 24])

# X3 = keepColumns(X, [24, 34, 17, 19])
X3 = preprocessing.scale(X3)
y_temp = y_new
# print y_temp.shape
# print X3.shape
data = np.insert(X3, X3.shape[1], y_temp, axis = 1)
corr = np.corrcoef(data.T)
pcolor(corr)
colorbar()

yticks(np.arange(0.5,5.5),range(0,10))
xticks(np.arange(0.5,5.5),range(0,10))
show()
#46: Well controlled by herbicides
#32: Self-compatible or apomictic
#24: Forms dense thickets
#34: Reproduction by vegetation
sampleAndAverage(predictLR, "predictLR", sample_size, X3, y_new)
sampleAndAverage(predictRF, "predictRF", sample_size, X3, y_new)
# sampleAndAverage(predictLR, "predictLR", sample_size, X2_transform, y_new)
# sampleAndAverage(predictRF, "predictRF", sample_size, X2_transform, y_new)

# sampleAndAverage(predictLR, "predictLR", sample_size, X, y_new)
# x7 = pca_decomposition(generalist, y_new)
# x8 = pca_decomposition(noninvasivethreats, y_new)
# x9 = pca_decomposition(other, y_new)
# Xtransform4 = np.column_stack((x7, x8, x9))
# sampleAndAverage(predictLR, "predictLR trying with pca decomposition with 10 most important features from before, new y", sample_size, Xtransform4, y_new)


X3= X3 + np.random.normal(0, 0.1, (X3.shape[0], X3.shape[1]))
fig = plt.figure(1, figsize=(4, 3))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
plt.cla()



ax.scatter(X3[:, 0], X3[:, 1], X3[:, 2], c=y_new)

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])

plt.show()


# compareFeatures(X, y_new)
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