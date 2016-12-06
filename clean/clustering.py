import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MeanShift, SpectralClustering
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D


def get_pca(features, components=18):
  model = PCA(n_components=components)
  model.fit(features.T)
  return model.components_.T

# plot 2 principal components for clustering results
def plot_clustering(features, labels, predictions):
  colors = ['r', 'y', 'b', 'g']
  for f, p, l in zip(features, predictions, labels):
    plt.scatter(f[0], f[1], c=colors[p], marker='o' if l == 1 else '^')
  plt.title('Mean Shift Clustering', fontsize=20)
  plt.xlabel('Principal Component 1', fontsize=16)
  plt.ylabel('Principal Component 2', fontsize=16)
  plt.show()
  # plt.savefig('figures/meanshift_clustering.png')

# test kmeans clustering
def kmeans_clustering(features, labels, clusters=2):
  model = KMeans(n_clusters=clusters)
  predictions = model.fit_predict(features)
  
  print get_impurity(predictions, labels)
  plot_clustering(features, labels, predictions)

# test spectral clustering
def spectral_clustering(features, labels, clusters=2):
  # test different kernels
  model = SpectralClustering(n_clusters=clusters, affinity='nearest_neighbors')
  predictions = model.fit_predict(features)
  
  print get_impurity(predictions, labels)

# test mean shift clustering
def mean_shift_clustering(features, labels):
  model = MeanShift()
  predictions = model.fit_predict(features)
  
  print get_impurity(predictions, labels)
  plot_clustering(features, labels, predictions)
  
# test impurity for different number of clusters for kmeans
def get_num_clusters(features, labels):
  impurity = []
  for i in range(2, 10):
    impurity.append(kmeans_clustering(features, labels, i))

  plt.plot(range(2, 10), impurity)
  plt.title('KMeans Gini Impurity vs Number of Clusters', fontsize=20)
  plt.xlabel('Number of Clusters', fontsize=16)
  plt.ylabel('Gini Impurity', fontsize=16)
  plt.show()
  # plt.savefig('figures/kmeans_gini_impurity.png')

# calculate gini impurity
def get_impurity(clusters, labels):
  impurities = []
  accuracy = 0
  # impurity for each cluster
  for c in set(clusters):
    count = 0
    total = 0
    for i in range(len(clusters)):
      if clusters[i] == c:
        total += 1
        if labels[i] == 1:
          count += 1
    # impurities.append(float(count)/total)
    impurities.append(((float(count)/total)**2) + (((total-float(count))/total)**2))

  # average impurity among all clusters
  return np.sum(impurities)/len(set(clusters))


# Note:
# with 2 clusters one cluster should have a high proportion of 1's
# and the other should have a low proportion of 1's for successful
# clustering


features = np.genfromtxt('data/clustering_features.csv', delimiter=',')
labels = np.genfromtxt('data/clustering_labels.csv')
features = get_pca(features, 2)
# get_num_clusters(features, labels)

kmeans_clustering(features, labels, 4)
spectral_clustering(features, labels, 4)
mean_shift_clustering(features, labels)
