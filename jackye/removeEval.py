import csv

f1 = open("pier_full_data.csv", "r")
f2 = open("pier_full_labels.csv", "r")
f3 = open("pier_ne_data.csv", "w")
f4 = open("pier_ne_labels.csv", "w")

for _ in range(1377):
	line = f1.readline()
	label = f2.readline()
	if label != "1\n":
		f3.write(line)
		f4.write(label)

f1.close()
f2.close()
f3.close()
f4.close()