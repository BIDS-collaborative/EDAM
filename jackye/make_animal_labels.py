import pandas as pd
# from difflib import get_close_matches

df = pd.read_csv("invasive_all.csv", sep=",")
df['sci_name']
sci_names = set(df['sci_name'])

df2 = pd.read_csv("WR05.txt", sep="\t")

i = 0
for name in df2['MSW05_Binomial']:
	# matches = get_close_matches(name.lower(), sci_names)
	# if matches:
	# 	i = i+1
	# 	print(name, matches)
	if name.lower() in sci_names:
		i=i+1

print(i)
