import csv

f_newdata = open("newdata.csv")
newdata_reader = csv.reader(f_newdata, delimiter="\t")

def process_line(line):
	species_name = line[1].lower()
	valid_words = [w for w in species_name.split(" ") if w.isalpha()]
	return " ".join(valid_words)

from difflib import get_close_matches

invasive_list = list()
for line in newdata_reader:
	invasive_list.append(process_line(line))


f_olddata = open("pier_ne_data.csv")
olddata_reader = csv.reader(f_olddata, delimiter=",")


def find_perfect_match(name, lst):
	name_tokens = name.split(" ")
	for e in lst:
		print("  [fpm] exam", e)
		if all([t in e for t in name_tokens]):
			print(" [fpm] found", e)
			return e
	print (" [fpm] not found")
	return None
				
def match_species(line):
	species_name = " ".join(line[0].split("_"))
	matches = get_close_matches(species_name, invasive_list)
	print(species_name, "has matches:", matches)

	if len(matches) == 1:
		return matches[0]
	elif matches:
		return find_perfect_match(species_name, matches)
		

invasive_total, total = 0, 0
f_labels = open("pier_ne_labels_new.csv", "w")

for line in olddata_reader:

	total += 1
	best_match = match_species(line)
	if best_match:
		invasive_total += 1
		f_labels.write("1\n")
	else:
		f_labels.write("0\n")

print(invasive_total, total, invasive_total/float(total))



f_newdata.close()
f_olddata.close()
f_labels.close()