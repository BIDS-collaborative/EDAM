'''
Author: Jack Ye
readPDF util, calls `pdftotext` command line util from Apache Xpdf to convert to txt
then parse line by line and record everything into featureMap (no record column puts NA)
'''

import re, os
from scoreMap import SCORE_MAP


# make sure in download phase the file name has no space
def getTextName(pdfPath):
	return pdfPath[:-3] + "txt"

def generateText(pdfPath, textPath):
	try:
		os.system("pdftotext -table {} {}".format(pdfPath, textPath))
		return True
	except:
		return False

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
			dic[featureID] = score
		else:
			dic[featureID] = "NA"

def reachEnd(tokens):
	return tokens[0] == "Designation:"

def calculateScore(featureDict):
	return 


def readPDF(pdfPath, featureDict):

	textPath = getTextName(pdfPath)

	if True or generateText(pdfPath):

		file = open(textPath, encoding="ISO-8859-1")

		for line in file:

			tokens = [s for s in re.split("\s+", line) if s]

			if tokens:
				if isTableLine(tokens):
					# print(tokens)
					analyzeTableLine(featureDict, tokens)
				elif reachEnd(tokens):
					return

	else:
		print("Please make sure Xpdf installed and pdfPath correct")


def main():
	nameDict, featureDict, scoreDict = dict(), dict(), dict()
	readPDF("test.pdf", featureDict)

	for k in sorted(featureDict.keys()):
		print(">>", k, ":", featureDict[k])
	print(sum([v for v in featureDict.values() if v != "NA"]))

if __name__ == '__main__':
	main()
	


















