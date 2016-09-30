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
	#Seems like the table we want is always the first or second table in the page. 
	if len(tables) == 1:
		table = tables[0]
	else:
		table = tables[1]
	result = table.find_all("tr")
	#Skip the first and potentially second row of table since they give no information.  	
	rows = result[: len(result) - 1]
	entries = rows[0].find_all("td")
	while len(entries) == 0:
		rows = rows[1:]
		entries = rows[0].find_all("td")
	if len(entries) >= 3:
		while entries[0].text.strip().encode("utf-8") != "1.01" and entries[2].text.strip().encode("utf-8") != "1.01":
			rows = rows[1:]
			entries = rows[0].find_all("td")
			while len(entries) < 3:
				rows = rows[1:]
				entries = rows[0].find_all("td")
	else: 
		while entries[0].text.strip().encode("utf-8") != "1.01":
			rows = rows[1:]
			entries = rows[0].find_all("td")

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
		elif len(entries) == 5 and entries[0].text.strip().encode("utf-8") == "":
			columns.append(entries[2].text.strip().encode('utf-8'))
			columns.append(entries[3].text.strip().encode('utf-8'))
			columns.append("")
			columns.append(entries[4].text.strip().encode('utf-8')) 
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
		print specie
		row = scrape(specie)
		if row is not None:
			matrix.append(row)
	matrix = np.array(matrix)
	with open('test.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerows(matrix)
	return matrix

species = getSpecies()

matrix = makeCSV()

# url = "http://www.hear.org/pier/wra/pacific/" + "mansoa_hymenaea" + "_htmlwra.htm"
# soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
# table = soup.find("table", attrs={"cellpadding":"2", "cellspacing":"0"})
# rows = table.find_all("tr")[1:]