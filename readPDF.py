'''
Author: Jack Ye
readPDF util, calls `pdftotext` command line util from Apache Xpdf to convert to txt
then parse line by line and record everything into featureMap (no record column puts NA)
'''

import re, os, json, csv, urllib.request
from scoreMap import SCORE_MAP


URL = "http://www.hear.org/pier/"
JSON_FILE = "plantpdfs.json"
CSV_PATH = "pier_data_wide.csv"
DATA_DIR = "data"


def getTextName(pdfPath):
	return pdfPath[:-3] + "txt"

def getPlantName(pdfPath):
	return pdfPath[:-4]


def generateText(pdfPath, textPath):
	try:
		os.system("pdftotext -table {} {}".format(pdfPath, textPath))
	except:
		print("Please make sure Xpdf installed and pdfPath correct")


def isTableLine(tokens):
	try:
		float(tokens[0])
		return len(tokens) > 1
	except:
		return False


def analyzeTableLine(dic, tokens):
	try:
		featureID = int(tokens[0])
	except:
		featureID = int(float(tokens[0]) * 100)

	if featureID == 301 and tokens[-1] == "n":
		dic[featureID] = dic[205]
	else:
		# print(tokens[-1], SCORE_MAP[featureID])
		score = SCORE_MAP[featureID].get(tokens[-1])
		if score != None:
			dic[featureID] = (tokens[-1], score)
		else:
			dic[featureID] = ("NA", "NA")


def reachEnd(tokens):
	return tokens[0] == "Designation:"


def calculateScore(featureDict):
	return sum([v[1] for v in featureDict.values() if v != "NA"])


def writeToCsvTidyForm(csvPath, plant, featureDict):
	print("	Writing",plant,"data to csv file")
	with open(csvPath, 'a') as file:
		for k in sorted(featureDict.keys()):
			lst = [str(i) for i in [plant, k] + list(featureDict[k])]
			file.write(",".join(lst))
			file.write("\n")


def writeToCsvWideForm(csvPath, plant, featureDict):
	print("	Writing",plant,"data to csv file")
	with open(csvPath, 'a') as file:
		file.write(plant + ",")
		file.write(",".join([str(featureDict[k][1]) for k in featureDict.keys()]))
		file.write("\n")


def readPDF(txtPath):

	featureDict = dict()
	file = open(txtPath, encoding="ISO-8859-1")

	print("	Analyzing table lines")
	for line in file:
		tokens = [s for s in re.split("\s+", line) if s]
		if tokens:
			if isTableLine(tokens):
				analyzeTableLine(featureDict, tokens)
			elif reachEnd(tokens):
				return featureDict



def importFiles(jsonFile):
	data = json.load(open(jsonFile))

	if not os.path.exists(DATA_DIR):
		os.makedirs(DATA_DIR)
	for line in data:
		fileName = line.split('/')[-1].replace("%20", '_')
		try:
			urllib.request.urlretrieve(URL + line, DATA_DIR + "/" + fileName)
			print("Downloaded:", fileName)
		except:
			print("**Failed download:", fileName)



def main():
	
	# importFiles(JSON_FILE)

	for f in os.listdir(DATA_DIR):
		try:
			print("START:", f)
			pdfName = DATA_DIR + "/" + f
			txtName = getTextName(pdfName)
			# generateText(pdfName, txtName)
			featureDict = readPDF(txtName)

			# for k in sorted(featureDict.keys()):
			# 	print(">>", k, ":", featureDict[k])
			# print(calculateScore(featureDict))
			writeToCsvWideForm(CSV_PATH, getPlantName(f), featureDict)
			print("	SUCCESSED", f)

		except:
			print("	FAILED", f)


if __name__ == '__main__':
	main()
	


















