import numpy as np
import matplotlib.pyplot as plt

from numpy import genfromtxt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# gathers the data from csv files
my_data = genfromtxt('pier_html_data_noevaluates.csv', delimiter=',')
my_labels = genfromtxt('pier_html_labels_noevaluates.csv', delimiter=',')

# changes all the NaN values to the mean of the column 
for array in my_data:
	mean = round(np.nanmean(array), 3)
	for index in range(len(array)):
		if np.isnan(array[index]):
			array[index] = mean



clf = RandomForestClassifier(n_estimators=10)


def chooseRandom(data, labels, size):
	"""Chooses test data and sample data randomly from the data"""
	x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size = size)
	return x_train, x_test, y_train, y_test 

def get_score(size, forest):
	"""Gets scores for RF based on varying test imputs"""
	x_train, x_test, y_train, y_test = chooseRandom(my_data, my_labels, size)
	rf = forest.fit(x_train, y_train)
	return rf.score(x_test, y_test)


def vary_forest_size(size, num_repeats, forests_varying_trees):
	"""Does RF many times, find the average score"""
	scores = []
	for forest in forests_varying_trees:
		total = 0
		for _ in range(num_repeats):
			total += get_score(size, forest)
		avg = total/num_repeats
		print("RF with a tree size of {}".format(forest.n_estimators) + ": ", avg)
		scores.append(avg)
	return scores

def vary_test_size(sizes, num_repeats, forest):
	"""Does RF many times, find the average score"""
	scores = []
	for size in sizes:
		total = 0
		for _ in range(num_repeats):
			total += get_score(size, forest)
		avg = total/num_repeats
		print("RF with a tree size of {}".format(size) + ": ", avg)
		scores.append(avg)
	return scores

def vary_max_feature(size, features, num_repeats):
	"""Does RF many times, find the average score"""
	scores = []
	for feature in features:
		total = 0
		clf = RandomForestClassifier(n_estimators=10, max_features = feature)
		for _ in range(num_repeats):
			total += get_score(size, clf)
		avg = total/num_repeats
		print("RF with a feature size of {}".format(feature) + ": ", avg)
		scores.append(avg)
	return scores

def plot_preduction_rates(x_axis, y_axis,title, x_label, y_label="prediction rate"):
	plt.plot(x_axis, y_axis)
	plt.xlabel(x_label)
	plt.ylabel("prediction rate")
	plt.ylim([0.8, 1.0])
	plt.title(title)
	print('done plotting!')
	plt.show()


num_repeats = 100
test_size = 0.25

#######################
# varying forest size #
#######################
forests_varying_trees = []
for num in range(201, 501, 50):
	forests_varying_trees.append(RandomForestClassifier(n_estimators=num))

forest_sizes = [forest.n_estimators for forest in forests_varying_trees]

title = '-------RF with a test size of {} and with {} repeats-------'.format(test_size, num_repeats)
print(title)
scores = vary_forest_size(test_size, num_repeats, forests_varying_trees)

plot_preduction_rates(forest_sizes, scores, title, "forest sizes")


#####################
# varying test size #
#####################
test_sizes = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]

title = '-------RF with a forest size of {} and with {} repeats-------'.format(10, num_repeats)
print(title)
scores = vary_test_size(test_sizes, num_repeats, clf)

plot_preduction_rates(test_sizes, scores, title, "test sizes")

########################
# varying max_features #
########################
num_features_considered = ['auto', 'sqrt', 'log2', None]

title = '-------RF with a forest size of {}, test size of {} and with {} repeats-------'.format(10, test_size, num_repeats)
print(title)
scores = vary_max_feature(test_size, num_features_considered, num_repeats)

plot_preduction_rates(num_features_considered, scores, title, "features")








