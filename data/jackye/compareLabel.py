
def percent_invasive(filepath):

	with open(filepath) as f:
		line = f.read()
		n = [int(i) for i in line.split("\n") if i != ""]

	return sum(n), len(n), sum(n) / float(len(n))

print(percent_invasive("pier_ne_labels.csv"))
print(percent_invasive("pier_ne_labels_new.csv"))