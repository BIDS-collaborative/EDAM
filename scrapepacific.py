import requests
import urllib2
from bs4 import BeautifulSoup
from lxml import html
import numpy as np
import pandas as pd
import sys
import csv

#Scrape information from the table for each species. Table in general has 4 colummns, with some rows having 3, so I added an extra blank column.
def scrape(species):
	species = species.replace(" ", "_")
	species = species.lower()
	url = "http://www.hear.org/pier/wra/pacific/" + species + "_htmlwra.htm"
	try:
		soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
	except urllib2.URLError:
		return None
	tables = soup.findAll("table")
	if len(tables) == 1:
		table = tables[0]
	else:
		table = tables[1]
	result = table.find_all("tr")
	if result[2].find_all("td")[0].text.strip().encode("utf-8") == "1.01":
		rows = result[1: len(result) - 1]
	else:
		rows = result[2: len(result) - 1]
	columns = [str(species)]
	for row in rows:
		entries = row.find_all("td")
		# r = np.array([entries[0].text, entries[1].text, entries[2].text, entries[3].text])
		# columns.append(r)
		# if len(entries) == 1: 
		# 	columns.append("")
		# 	columns.append("")
		# 	columns.append("")
		# 	columns.append(entries[0].text.strip().encode('utf-8'))
		if len(entries) == 2:
			columns.append(entries[0].text.strip().encode('utf-8'))
			columns.append("")
			columns.append("")
			columns.append(entries[1].text.strip().encode('utf-8'))
		elif len(entries) == 3:
			columns.append(entries[0].text.strip().encode('utf-8'))
			columns.append(entries[1].text.strip().encode('utf-8'))
			columns.append("")
			columns.append(entries[2].text.strip().encode('utf-8'))
		elif len(entries) >= 4: 
			columns.append(entries[0].text.strip().encode('utf-8'))
			columns.append(entries[1].text.strip().encode('utf-8'))
			columns.append(entries[2].text.strip().encode("utf-8"))
			columns.append(entries[3].text.strip().encode('utf-8'))

	return np.array(columns)


#Attempted to scrape the species names from the website itself, but failed. Using the csv for now. 
def getSpecies():
	# url = "http://www.hear.org/pier/wralist.htm"
	# soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
	# table = soup.find("table")
	# rows = table.find_all("tr")[1:]
	# species = []
	# for row in rows:
	# 	entries = row.find_all("td")
	# 	species.append(entries[0].text.strip())
	# return species
	df = pd.read_csv("pacificplants.csv")
	return df["Scientific Name"]

#Scrapes from the website and makes CSV.
def makeCSV():
	species = getSpecies()
	matrix = []
	for specie in species:
		row = scrape(specie)
		if row is not None:
			matrix.append(row)
	matrix = np.array(matrix)
	with open('Brianoutput.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerows(matrix)
	return matrix

# species = getSpecies()

matrix = makeCSV()

url = "http://www.hear.org/pier/wra/pacific/" + "funtumia_elastica" + "_htmlwra.htm"
soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
table = soup.find("table", attrs={"border":"2", "cellpadding":"2", "cellspacing":"0"})
rows = table.find_all("tr")[1:]