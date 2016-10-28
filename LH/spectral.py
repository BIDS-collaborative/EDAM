import pandas as pd, numpy as np, warnings, sklearn
from sklearn.cluster import KMeans, SpectralClustering
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.utils import shuffle

def load_data(fileName, dropFirstColumn = True):
	df = pd.read_csv(fileName)
	if dropFirstColumn:
		df = df.drop(df[[0]], axis = 1)
	return df.as_matrix()

def combineFeatureByMean(X, category):
	newX = np.empty([X.shape[0],len(category)-1])
	for i in range(len(category)-1):
		# print(category[i])
		nextX = X[:,category[i]:category[i+1]]
		# print(nextX.shape)
		newX[:,i] = np.nanmean(nextX, axis=1)
		# print(newX.shape)
	return newX

def predictSpectralClustering(X, y, n=2):
	#ranX, ranY = shuffle(X, y, random_state=0)
	X = X[:600,]
	y = y[:600,]
	sc = SpectralClustering(n_clusters=n)
	results = sc.fit_predict(X)
	gini = compute_gini(results)
	if n == 2:
		same = calculate_score(results, y)
		opp = calculate_score(results, y, True)
		return (results, max(same, opp), gini)
	else:
		return (results, 0, gini)

def calculate_score(predicted, actual, switch=False):
	score = 0
	if (predicted.shape == actual.shape):
		for i,j in zip(predicted, actual):
			if (i != j):
				if switch:
					score += 1
			else:
				if not switch:
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

sample_size = 50
category = [0, 3, 8, 13, 25, 29, 36, 44, 49]

warnings.filterwarnings('ignore')


X = load_data("pier_ne_data.csv")
col_mean = np.nanmean(X,axis=0)
inds = np.where(np.isnan(X))
X[inds]=np.take(col_mean,inds[1])

X_comb = combineFeatureByMean(X, category)

y = np.divide(np.ravel(load_data("pier_ne_labels.csv", False)), 2)

print("--------------NE DATA SET SPECTRAL-----------------")

results, score, gini = predictSpectralClustering(X,y)
print score

# Create a PCA model.
pca_2 = PCA(2)
# Fit the PCA model on the numeric columns from earlier.
plot_columns = pca_2.fit_transform(X)
# Make a scatter plot of each game, shaded according to cluster assignment.
plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=results)
# Show the plot.
plt.show()

cluster_size = [2, 4, 6, 8, 10]
gini = []
for c in cluster_size:
	vals = predictSpectralClustering(X,y,c)
	gini.append(vals[2])

print("PLOT CLUSTERS V. GINI")
plt.plot(cluster_size, gini)
plt.xlabel("num clusters")
plt.ylabel("gini")
plt.axis([2, 10, 0, 1])
plt.show()


