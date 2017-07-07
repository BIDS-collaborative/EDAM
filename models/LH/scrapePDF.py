'''
Author: Lavanya Harinarayan
Scrapes data from the second type of pdf (/tncflwra) using Apache xPDF
'''
import json, requests, os, re

JSON_FILE = "plantpdfs2.json"
DATA_DIR = "data"
QUESTIONS = ['1.01', '1.02', '1.03', '2.01', '2.02', '2.03', '2.04', '2.05', 
'3.01', '3.02', '3.03', '3.04', '3.05', 
'4.01', '4.02', '4.03', '4.04', '4.05', '4.06', '4.07', '4.08', '4.09', '4.1', '4.11', '4.12',
'5.01', '5.02', '5.03', '5.04',
'6.01', '6.02', '6.03', '6.04', '6.05', '6.06', '6.07',
'7.01', '7.02', '7.03', '7.04', '7.05', '7.06', '7.07', '7.08',
'8.01', '8.02', '8.03', '8.04', '8.05']


def importPDFs(JSON_FILE): #Based on Jack Ye's importFiles
	if not os.path.exists(DIR):
		os.makedirs(DIR)

	with open(JSON_FILE) as datafile:    
		data = json.load(datafile)
	for url in data:
		try:
			r = requests.get(url)
			fileURL = url[47:].split('/')[-1].replace("%20", '_')
			fileName = os.path.join(DIR, fileURL)         
			with open(fileName, 'wb') as f:
				f.write(r.content)
			print("Downloaded:", fileName)
		except:
			print("***FAILED:", fileName)

def test_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def isFeature(tokens):
	return tokens[0] in QUESTIONS

def isScoreLine(tokens):
	return tokens[0]=="Total" and tokens[1]=="Score"

def read_txt(txtPath):
	""" Reads .txt file to create a dict where k = feature & value = 0,1"""
	featureDict = dict()
	path = DATA_DIR + "/" + txtPath
	file = open(path)

	for line in file:
		tokens = [s for s in re.split("\s+", line) if s]
		if tokens:
			val = "NA"
			if test_int(tokens[-1]):
				val = tokens[-1]
			if isFeature(tokens):
				featureDict[tokens[0]] = val
			elif isScoreLine(tokens):
				featureDict["Score"] = val
				return featureDict

def write_to_CSV(name, featureDict):
	score = featureDict["Score"]
	if test_int(score):
		with open("plantpdfsfeatures.csv", 'a') as file:
			lst = [name]
			for q in QUESTIONS:
				if (q in featureDict):
					lst.append(featureDict[q])
				else:
					lst.append("NA")
			file.write(",".join(lst))
			file.write("\n")
		with open("plantpdfslabel.csv", 'a') as file:
			if int(score) < 1:
				val = "0"
			elif int(score) > 6:
				val = "2"
			else:
				val = "1"
			file.write(val)
			file.write("\n")

def getPlantName(txt_path):
	name = txt_path[:-4].replace("_", ' ')
	return name

def createCSV():
	with open("plantpdfs2.csv", 'a') as file:
		lst = ["Name", "Score"]
		lst.extend(QUESTIONS)
		file.write(",".join(lst))
		file.write("\n")

def main():
	# importPDFs(JSON_FILE)
	# for f in os.listdir(DATA_DIR):
	# 	pdfPath = DATA_DIR + "/" + f
	# 	textPath = getTextName(pdfPath)
	# 	generateText(pdfPath, textPath)
	#createCSV()
	for f in os.listdir(DATA_DIR):
		features = read_txt(f)
		if features:
			write_to_CSV(getPlantName(f), features)
	#print(read_txt("data/abrus_precatorius_ispm.txt"))

if __name__ == '__main__':
	main()
