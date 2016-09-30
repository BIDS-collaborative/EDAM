# Author: Lavanya Harinarayan
# Scrapes "http://www.hear.org/pier/wralist.htm" 
# Gets list of all plant names, URLs that lead to PDFs of plant risk assessment

from bs4 import BeautifulSoup
import json
import requests

r = requests.get('http://www.hear.org/pier/wralist.htm')
soup = BeautifulSoup(r.text, 'lxml')

#GET URLS
data = []
for link in soup.find_all('a'):
	data.append(link.get('href'))

data = [d for d in data if d[0:11]=="wra/pacific" and d[-3:]=="pdf"]

with open('plantpdfs.json', 'w') as savefile:
	json.dump(data, savefile, indent=4, separators=(',', ':'))

#GET NAMES
table = soup.find('table')
rows = table.find_all('tr')
data = [row.find_all('td')[3] for row in rows]

data = [' '.join(d.replace('\r\n', '').split()) for d in data]

with open('plantnames.json', 'w') as savefile:
	json.dump(data, savefile, indent=4, separators=(',', ':'))