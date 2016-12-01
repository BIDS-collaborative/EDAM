import requests, re, json, io, os, urllib
from bs4 import BeautifulSoup
from lxml import html

VAL_LOOKUP = {'y': 1, 'n': 0, 'High': 2, 'Intermediate': 1, 'Low': 0}


# scrape plant data
def scrape_pacific_plants_names():
  r = requests.get('http://www.hear.org/pier/wralist.htm')
  html = BeautifulSoup(r.text, 'lxml')

  table = html.find('table')
  # remove header row
  rows = table.find_all('tr')[1:]
  
  # find scientific names
  data = [row.find_all('td')[0] for row in rows]
  plant_scientific_names = []
  # clean parsed data
  for d in data:
    plant_scientific_names.append(re.sub('[\s]+', ' ', re.sub('^[\s]+|[\s]+$|[\r\n]', '' , re.sub('<.*?>', '', str(d)))))

  # write names to json
  with open('plant_scientific_names.json', 'w') as datafile:
    json.dump(plant_scientific_names, datafile, indent=2, separators=(',', ':'))

  # find common names
  data = [row.find_all('td')[2] for row in rows]
  plant_common_names = []
  # clean parsed data
  for d in data:
    plant_common_names.append(re.sub('[\s]+', ' ', re.sub('^[\s]+|[\s]+$|[\r\n]', '' , re.sub('<.*?>', '', str(d)))))

  # write names to json
  with open('plant_common_names.json', 'w') as datafile:
    json.dump(plant_common_names, datafile, indent=2, separators=(',', ':'))


def scrape_pacific_plants_location():
  r = requests.get('http://www.hear.org/pier/wralist.htm')
  html = BeautifulSoup(r.text, 'lxml')

  table = html.find('table')
  # remove header row
  rows = table.find_all('tr')[1:]
  
  # find scientific names
  data = [row.find_all('td')[4] for row in rows]
  plant_location = []
  # clean parsed data
  for d in data:
    plant_location.append(re.sub('[\s]+', ' ', re.sub('^[\s]+|[\s]+$|[\r\n]', '' , re.sub('<.*?>', '', str(d)))))

  # write locations to json
  with open('plant_locations.json', 'w') as datafile:
    json.dump(plant_location, datafile, indent=2, separators=(',', ':'))


def scrape_pacific_plants_links():
  r = requests.get('http://www.hear.org/pier/wralist.htm')
  html = BeautifulSoup(r.text, 'lxml')

  table = html.find('table')
  # remove header row
  rows = table.find_all('tr')[1:]
  
  # find scientific names
  data = [row.find_all('td')[3] for row in rows]
  plant_links = []
  for d in data:
    plant_links.append(d.find('a').get('href'))

  # write links to json
  with open('plant_links.json', 'w') as datafile:
    json.dump(plant_links, datafile, indent=2, separators=(',', ':'))


def scrape_pacific_plants_html(link):
  return

def is_table_line(tokens):
  try: 
    float(tokens[0])
    return len(tokens) > 1
  except:
    return False

def is_table_end(tokens):
  return tokens[0] == 'Designation:' or (tokens[0] == 'Total' and tokens[1] == 'Score')


def scrape_pacific_plants_pdf(link):
  # create temp file
  pdfname = link.split('/')[-1].replace('%20', '_')
  txtname = re.sub('.pdf', '.txt', pdfname)

  alt = False
  if re.search('tncflwra', pdfname) is not None:
    alt = True

  # download link to temp file
  try:
    urllib.urlretrieve(link, pdfname)
  except:
    print 'Failed to download: {}'.format(pdfname)

  # convert pdf to txt
  # requires installation of xpdf
  try:
    os.system('pdftotext -table {} {}'.format(pdfname, txtname))
    os.system('rm {}'.format(pdfname))
  except:
    print 'Please make sure Xpdf is installed and pdfPath is correct'

  # parse pdf content
  feature_dict = dict()
  with io.open(txtname, encoding='ISO-8859-1') as pdffile:
    for line in pdffile:
      tokens = [t for t in re.split('\s+', line) if t]
      if tokens:
        if is_table_line(tokens):

          # convert question to integer key
          try:
            feature_id = int(tokens[0])
          except:
            feature_id = int(round(float(tokens[0]) * 100))

          # alternate pdf format
          if alt:
            # edge cases
            if feature_id in [201, 202, 607]:
              try:
                feature_dict[feature_id] = int(tokens[-1])
              except:
                feature_dict[feature_id] = 'NA'
            # lookup Y/N values
            else:
              if tokens[-1] in VAL_LOOKUP:
                feature_dict[feature_id] = VAL_LOOKUP[tokens[-1]]
              elif tokens[-2] in VAL_LOOKUP:
                feature_dict[feature_id] = VAL_LOOKUP[tokens[-2]]
              else:
                feature_dict[feature_id] = 'NA'
          else:
            # lookup values
            if tokens[-1] in VAL_LOOKUP:
              feature_dict[feature_id] = VAL_LOOKUP[tokens[-1]]
            # edge numeric cases
            else:
              try:
                feature_dict[feature_id] = int(tokens[-1])
              except:
                feature_dict[feature_id] = 'NA'
        
        # end of questions
        elif is_table_end(tokens):
          break

  # remove temp file
  os.system('rm {}'.format(txtname))
  return feature_dict


def scrape_pacific_plants_data():
  plant_links = json.load(open('plant_links.json'))
  plant_data = []

  for link in plant_links:
    if re.search('.*?.htm', link) is not None:
      plant_data.append(scrape_pacific_plants_html(link))
    elif re.search('.*?.pdf', link) is not None:
      plant_data.append(scrape_pacific_plants_pdf(link))

# def join_pacific_plants():
  

# # subset pacific plants, remove no eval/no score
# def clean_pacific_plants():


# # read lists of invasive plants
# def scrape_invasive_plants():


# # match plant data with invasive plants
# def label_pacific_plants():

print scrape_pacific_plants_pdf('http://www.hear.org/pier/wra/pacific/Abelmoschus%20manihot.pdf')
# print scrape_pacific_plants_pdf('http://www.hear.org/wra/tncflwra/pdfs/tncflwra_abrus_precatorius_ispm.pdf')