import sys
import pandas as pd
import numpy as np
import warnings
import sklearn
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import app.webtool.views as wt

sys.path.insert(0, '../..')
data = "../../app/documents/pacific_plant_data.csv"
label = "../../app/documents/pacific_plant_label.csv"

def load_data(fileName, dropFirstColumn = True):
    df = pd.read_csv(fileName)
    if dropFirstColumn:
        df = df.drop(df[[0]], axis = 1)
    return df.as_matrix()

def combineFeatureByMean(X, category):
    newX = np.empty([X.shape[0], len(category) - 1])
    for i in range(len(category) - 1):
        # print(category[i])
        nextX = X[:, category[i]:category[i + 1]]
        # print(nextX.shape)
        newX[:, i] = np.nanmean(nextX, axis=1)
        # print(newX.shape)
    return newX

def predictKMeans(X, y, n):
    col_mean = np.nanmean(X,axis=0)
    inds = np.where(np.isnan(X))
    X[inds]=np.take(col_mean,inds[1])
    km = KMeans(n_clusters=n)
    X_train, X_test, y_train, y_test = chooseRandom(X, y)
    km.fit(X_train)
    results = km.predict(X_test)
    collapsed = collapse_clusters(results, n)
    score = calculate_score(collapsed, y_test)
    gini = compute_gini(results)
    return (score, gini)

def collapse_clusters(matrix, n):
    mid = n/2
    for i in range(0, matrix.shape[0]):
        if (matrix[i,] < mid):
            matrix[i,] = 0
        else:
            matrix[i,] = 1
    return matrix

def calculate_score(predicted, actual):
    score = 0
    if (predicted.shape == actual.shape):
        for i,j in zip(predicted, actual):
            if (i == j):
                score += 1
        return float(score)/predicted.shape[0]
    else:
        return None

def sampleAndAverage(method, method_string, iterations, X, y, n):
    # print("[{}] start score calculation for {} iterations".format(method_string, iterations))
    score = 0
    gini = 0
    for _ in range(iterations):
        col_mean = np.nanmean(X,axis=0)
        inds = np.where(np.isnan(X))
        X[inds]=np.take(col_mean,inds[1])
        vals = method(X, y, n)
        score += vals[0]
        gini += vals[1]
    print("[{}] average score: {}".format(method_string, score/iterations))
    print("[{}] average gini: {}".format(method_string, gini/iterations))
    return (score/iterations, gini/iterations)


def compute_gini(predicted):
    total = float(predicted.shape[0])
    giniDict = {}
    for val in predicted:
        if val in giniDict:
            giniDict[val] += 1
        else:
            giniDict.update({val:1})
    gini = 0
    for key in giniDict:
        f = giniDict[key]/total
        gini += f*(1-f)
    return gini

def chooseRandom(x, y):
    x_train, x_test, y_train, y_test = sklearn.cross_validation.train_test_split(x, y, test_size = 0.5)
    return x_train, x_test, y_train, y_test

sample_size = 50
category = [0, 3, 8, 13, 25, 29, 36, 44, 49]

warnings.filterwarnings('ignore')


X = load_data("pier_ne_data.csv")
X_comb = combineFeatureByMean(X, category)
y = np.divide(np.ravel(load_data("pier_ne_labels.csv", False)), 2)

print("--------------NE DATA SET KMEANS-----------------")



cluster_size = [2, 4, 6, 8, 10]
score = []
gini = []
for c in cluster_size:
    vals = sampleAndAverage(predictKMeans,
                            "KMeans Clustering, NE data set", sample_size, X_comb, y, c)
    score.append(vals[0])
    gini.append(vals[1])

print(score)
print(gini)

print("PLOT CLUSTERS V. SCORE")
plt.plot(cluster_size, score)
plt.xlabel("num clusters")
plt.ylabel("score")
plt.axis([2, 10, 0, 1])
plt.show()

print("PLOT CLUSTERS V. GINI")
plt.plot(cluster_size, gini)
plt.xlabel("num clusters")
plt.ylabel("gini")
plt.axis([2, 10, 0, 1])
plt.show()


# print sampleAndAverage(predictKMeans, "KMeans Clustering, NE data set", sample_size, X, y)
