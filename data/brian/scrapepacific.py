import requests
import urllib2
from bs4 import BeautifulSoup
from lxml import html
import numpy as np
import pandas as pd
import sys
import csv
from scoreMap import SCORE_MAP
import re

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
    #Skip until the first row with info 
    rows = result[: len(result) - 1]
    entries = rows[0].find_all("td")
    while len(entries) == 0:
        rows = rows[1:]
        entries = rows[0].find_all("td")
    edgeCase = False
    if len(entries) >= 3:
        if entries[2].text.strip().encode("utf-8") == "1.01":
            edgeCase = True
        while entries[0].text.strip().encode("utf-8") != "1.01" and entries[2].text.strip().encode("utf-8") != "1.01":
            rows = rows[1:]
            entries = rows[0].find_all("td")
            if len(entries) >= 3:
                if entries[2].text.strip().encode("utf-8") == "1.01":
                    edgeCase = True
            while len(entries) < 3:
                rows = rows[1:]
                entries = rows[0].find_all("td")
                if len(entries) >= 3:
                    if entries[2].text.strip().encode("utf-8") == "1.01":
                        edgeCase = True

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
        #   columns.append("")
        #   columns.append("")
        #   columns.append("")
        #   columns.append(entries[0].text.strip().encode('utf-8'))
        if edgeCase:
            if len(entries) == 5:
                columns.append(entries[2].text.strip().encode('utf-8'))
                columns.append(entries[3].text.strip().encode('utf-8'))
                columns.append("")
                columns.append(entries[4].text.strip().encode('utf-8'))             
        elif len(entries) == 2:
            columns.append(entries[0].text.strip().encode('utf-8'))
            columns.append("")
            columns.append("")
            columns.append(entries[1].text.strip().encode('utf-8'))
        elif len(entries) == 3:
            columns.append(entries[0].text.strip().encode('utf-8'))
            columns.append(entries[1].text.strip().encode('utf-8'))
            columns.append("")
            columns.append(entries[2].text.strip().encode('utf-8'))
        #Want y or n or etc on last column, not score. Score we can calculate ourselves
        elif len(entries) >= 4: 
            if len(entries[2].text.strip().encode("utf-8")) > 4 or len(entries[2].text.strip().encode("utf-8")) == 0:
                columns.append(entries[0].text.strip().encode('utf-8'))
                columns.append(entries[1].text.strip().encode('utf-8'))
                columns.append(entries[2].text.strip().encode("utf-8"))
                columns.append(entries[3].text.strip().encode('utf-8'))
            else:
                columns.append(entries[0].text.strip().encode('utf-8'))
                columns.append(entries[1].text.strip().encode('utf-8'))
                columns.append("")              
                columns.append(entries[2].text.strip().encode("utf-8"))

    return np.array(columns)


#Attempted to scrape the species names from the website itself, but failed. Using the csv for now. 
def getSpecies():
    # url = "http://www.hear.org/pier/wralist.htm"
    # soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
    # table = soup.find("table")
    # rows = table.find_all("tr")[1:]
    # species = []
    # for row in rows:
    #   entries = row.find_all("td")
    #   species.append(entries[0].text.strip())
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

def cleanData():
    m = pd.read_csv("test.csv", header = None)
    drop = []
    for i in range(241):
        if i % 4 == 2 or i % 4 == 3 or i > 196:
                drop.append(i)
    matrix = m.drop(m[drop], axis = 1)
    matrix = matrix.as_matrix()
    newMatrix = []
    for j in range(matrix.shape[0]):
        row = [matrix[j][0]]
        i = 1
        while i < matrix.shape[1]:
            label = matrix[j][i]
            label = int(round(float(label) * 100))
            value = matrix[j][i + 1]
            if label != 607:
                try:
                    value = float(value)
                    if value != value:
                        score = "NA"
                    else:
                        score = int(value)
                except ValueError:
                    value = value.lower()
                    if value == "no":
                        value = "n"
                    if value == "yes":
                        value = "y"
                    try: 
                        score = SCORE_MAP[label][value]
                    #greedily finds first score 
                    except KeyError:
                        score = "" 
                        foundNumber = False
                        for c in value:
                            if c.isdigit():
                                foundNumber = True
                                score += c
                            else: 
                                if foundNumber:
                                    break
                        if foundNumber:
                            score = int(score)
                        else:
                            score = "NA"
            else:
                try:
                    value = float(value)
                    if value != value:
                        score = "NA"
                    else:
                        score = int(value)
                except ValueError:
                    value = "" 
                    foundNumber = False
                    for c in value:
                        if c.isdigit():
                            foundNumber = True
                            value += c
                        else: 
                            if foundNumber:
                                break
                        value = int(value)
                    if value > 3:
                        value = ">3"
                    value = str(value)
                    score = SCORE_MAP[label][value]

            row.append(score)
            i += 2
        newMatrix.append(np.array(row))
    newMatrix = np.array(newMatrix)
    return newMatrix


# species = getSpecies()

# matrix = makeCSV()

# url = "http://www.hear.org/pier/wra/pacific/" + "ischaemum_polystachyum" + "_htmlwra.htm"
# specie = scrape("ischaemum_polystachyum")
# soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
# table = soup.find("table", attrs={"cellpadding":"2", "cellspacing":"0"})
# rows = table.find_all("tr")[1:]


