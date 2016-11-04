import urllib.request
from bs4 import BeautifulSoup as BS

site = "http://bonap.net"
page = urllib.request.urlopen("http://bonap.net/NAPA/Genus/Traditional/State")
soup = BS(page)

def getnames(href, file):
	print("getnames:", href)
	pg = urllib.request.urlopen(href)
	sp = BS(pg)
	for tr in sp.find_all("tr"):
		for div in tr.find_all("div"):
			print(div.text)
			file.write(div.text.lower())
			file.write("\n")

f = open("all_plants.csv", "w")

for tr in soup.find_all("tr"):
	for a in tr.find_all("a", href=True):
		try:
			getnames(site + a['href'], f)
		except:
			pass

f.close()