import pandas as pd, numpy as np, warnings, sklearn
from sklearn.cluster import AffinityPropagation, DBSCAN, MeanShift, estimate_bandwidth
from sklearn.decomposition import PCA
from sklearn import metrics
import matplotlib.pyplot as plt
from itertools import cycle

def load_data(fileName, dropFirstColumn = True):
	df = pd.read_csv(fileName)
	if dropFirstColumn:
		df = df.drop(df[[0]], axis = 1)
	return df.as_matrix()

def predictAffinityPropagation(X, labels_true):
	#ranX, ranY = shuffle(X, y, random_state=0)
	af = AffinityPropagation(preference=-50).fit(X)
	cluster_centers_indices = af.cluster_centers_indices_
	labels = af.labels_

	n_clusters_ = len(cluster_centers_indices)

	print('Estimated number of clusters: %d' % n_clusters_)
	print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
	print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
	print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
	print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
	print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
	print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels, metric='sqeuclidean'))

	plt.close('all')
	plt.figure(1)
	plt.clf()

	colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
	for k, col in zip(range(n_clusters_), colors):
	    class_members = labels == k
	    cluster_center = X[cluster_centers_indices[k]]
	    plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
	    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
	             markeredgecolor='k', markersize=14)
	    for x in X[class_members]:
	        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

	plt.title('Estimated number of clusters: %d' % n_clusters_)
	plt.show()

def predictDBSCAN(X, labels_true):
	db = DBSCAN(eps=0.3, min_samples=10).fit(X)
	core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True
	labels = db.labels_

	# Number of clusters in labels, ignoring noise if present.
	n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

	# print('Estimated number of clusters: %d' % n_clusters_)
	# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
	# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
	# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
	# print("Adjusted Rand Index: %0.3f"
	#       % metrics.adjusted_rand_score(labels_true, labels))
	# print("Adjusted Mutual Information: %0.3f"
	#       % metrics.adjusted_mutual_info_score(labels_true, labels))
	# print("Silhouette Coefficient: %0.3f"
	#       % metrics.silhouette_score(X, labels))
	# Black removed and is used for noise instead.
	unique_labels = set(labels)
	colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
	for k, col in zip(unique_labels, colors):
	    if k == -1:
	        # Black used for noise.
	        col = 'k'

	    class_member_mask = (labels == k)

	    xy = X[class_member_mask & core_samples_mask]
	    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
	             markeredgecolor='k', markersize=14)

	    xy = X[class_member_mask & ~core_samples_mask]
	    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
	             markeredgecolor='k', markersize=6)

	plt.title('Estimated number of clusters: %d' % n_clusters_)
	plt.show()

def predictMeanShift(X, labels):
	# The following bandwidth can be automatically detected using
	bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)

	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
	results = ms.fit_predict(X)
	print list(results)
	labels = ms.labels_
	cluster_centers = ms.cluster_centers_

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)

	print("number of estimated clusters : %d" % n_clusters_)
	# Create a PCA model.
	pca_2 = PCA(2)
	# Fit the PCA model on the numeric columns from earlier.
	plot_columns = pca_2.fit_transform(X)
	# Make a scatter plot of each game, shaded according to cluster assignment.
	plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=results)
	plt.title("Mean Shift- 4 clusters")
	# Show the plot.
	plt.show()

warnings.filterwarnings('ignore')


X = load_data("pier_ne_data.csv")
col_mean = np.nanmean(X,axis=0)
inds = np.where(np.isnan(X))
X[inds]=np.take(col_mean,inds[1])


y = np.divide(np.ravel(load_data("pier_ne_labels.csv", False)), 2)


print predictMeanShift(X, y)

