import requests, re, json, io, os, urllib, csv
import numpy as np
from bs4 import BeautifulSoup
from lxml import html

VAL_LOOKUP = {'y': 1, 'n': 0, 'High': 2, 'Intermediate': 1, 'Low': 0}
EDGE_CASES = [201, 202, 607]


def parse_html(html):
  return re.sub('[\s]+', ' ', re.sub('^[\s]+|[\s]+$|[\r\n]', '' , re.sub('<.*?>', '', html)))

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
    plant_scientific_names.append(parse_html(str(d)))

  # write names to json
  with open('data/plant_scientific_names.json', 'w') as datafile:
    json.dump(plant_scientific_names, datafile, indent=2, separators=(',', ':'))

  # find common names
  data = [row.find_all('td')[2] for row in rows]
  plant_common_names = []
  # clean parsed data
  for d in data:
    plant_common_names.append(parse_html(str(d)))

  # write names to json
  with open('data/plant_common_names.json', 'w') as datafile:
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
    plant_location.append(parse_html(str(d)))

  # write locations to json
  with open('data/plant_locations.json', 'w') as datafile:
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
  with open('data/plant_links.json', 'w') as datafile:
    json.dump(plant_links, datafile, indent=2, separators=(',', ':'))


def scrape_pacific_plants_html(link):
  if re.search('http', link) is None:
    link = 'http://www.hear.org/pier/' + link

  r = requests.get(link)
  html = BeautifulSoup(r.text, 'lxml')

  # check Australian table format
  question_index = 0
  answer_index = -1
  aus = False
  try:
    table = html.find_all('table')[1]
  except:
    table = html.find_all('table')[0]
    aus = True
    question_index = 2

  rows = table.find_all('tr')
  header = rows[0]
  rows = rows[1:-1]

  # check for score column
  if parse_html(str(header.find_all('td')[-1])) == 'Score':
    answer_index -= 1

  feature_dict = dict()
  for row in rows:
    data = row.find_all('td')
    # end of Australian table
    if aus and parse_html(str(data[3])) == 'Outcome:':
      break

    # check if feature row
    try:
      feature_id = int(round(float(parse_html(str(data[question_index]))) * 100))
    except:
      continue

    answer = parse_html(str(data[answer_index])).lower()

    if feature_id in EDGE_CASES:
      try:
        feature_dict[feature_id] = int(answer)
      except:
        feature_dict[feature_id] = 'NA'
    else:
      if answer in VAL_LOOKUP:
        feature_dict[feature_id] = VAL_LOOKUP[answer]
      else:
        feature_dict[feature_id] = 'NA'
    
  return feature_dict


def is_table_line(tokens):
  try: 
    float(tokens[0])
    return len(tokens) > 1
  except:
    return False

def is_table_end(tokens):
  return tokens[0] == 'Designation:' or (tokens[0] == 'Total' and tokens[1] == 'Score')

# need to fix florida (tncflwra)
def scrape_pacific_plants_pdf(link):
  if re.search('http', link) is None:
    link = 'http://www.hear.org/pier/' + link

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
    return

  # convert pdf to txt
  # requires installation of xpdf
  try:
    os.system('pdftotext -table {} {}'.format(pdfname, txtname))
    os.system('rm {}'.format(pdfname))
  except:
    print 'Please make sure Xpdf is installed and pdfPath is correct'
    return

  # parse pdf content - extract answer to questions, not score value
  feature_dict = dict()
  # catch file open exception
  try:
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
              if feature_id in EDGE_CASES:
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
  except:
    return feature_dict

  return feature_dict

def write_to_csv(csv_name, data):
  with open(csv_name, 'a') as csvfile:
    csvfile.write(data.encode('utf-8').strip() + '\n')


def scrape_pacific_plants_data():
  # load link and name data files
  plant_links = json.load(open('data/plant_links.json'))
  plant_names = json.load(open('data/plant_scientific_names.json'))
  
  # match name and scrape data from link
  for link, name in zip(plant_links, plant_names):
    plant_data = {}
    print name
    if re.search('.*?.htm', link) is not None:
      plant_data = scrape_pacific_plants_html(link)
    elif re.search('.*?.pdf', link) is not None:
      plant_data = scrape_pacific_plants_pdf(link)

    # write data to csv
    write_to_csv('data/plant_data.csv', name + ',' + ','.join([str(plant_data[k]) for k in sorted(plant_data.keys())]))
  

# filter plants with missing data and by region (only Pacific)
def clean_pacific_plants():
  # load location data file
  plant_locations = json.load(open('data/plant_locations.json'))

  # check location and data completeness and write to file
  with open('data/plant_data.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row, location in zip(csvreader, plant_locations):
      if location == 'Pacific' and len(row) == 50:
        write_to_csv('data/pacific_plant_data.csv', ','.join(row).decode('utf-8'))


# read lists of invasive plants
def scrape_invasive_plants():
  r = requests.get('http://www.invasiveplantatlas.org/distribution.html')
  html = BeautifulSoup(r.text, 'lxml')

  table = html.find('table')
  rows = table.find_all('tr')[1:]

  data = [row.find_all('td')[1] for row in rows]
  invasive_plants = []

  # parse html
  for d in data:
    invasive_plants.append(parse_html(str(d)))

  # write invasive plants to json
  with open('data/invasive_plants.json', 'w') as datafile:
    json.dump(invasive_plants, datafile, indent=2, separators=(',', ':'))


# match plant data with invasive plants
def label_pacific_plants():
  # load invasive plants data file
  invasive_plants = json.load(open('data/invasive_plants.json'))
  species_dict = {}

  # convert invasive plants list to genus:species dictionary
  for plant in invasive_plants:
    tokens = plant.split(' ')
    genus = str(tokens[0])
    species = str(tokens[1])
    # note: spp = all species of genus
    if species == 'x':
      species = tokens[2]
    
    if genus in species_dict.keys():
      species_dict[genus].append(species)
    else:
      species_dict[genus] = [species]

  # iterate through list of plants
  with open('data/pacific_plant_data.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    # check for match in invasive plants list
    for row in csvreader:
      tokens = row[0].split(' ')
      genus = tokens[0]
      if genus in species_dict.keys():
        species = tokens[1]
        if species == 'x':
          species = tokens[2]

        if species in species_dict[genus] or species_dict[genus] == 'spp.':
          write_to_csv('data/pacific_plant_label.csv', '1')
        else:
          write_to_csv('data/pacific_plant_label.csv', '0')
      else:
        write_to_csv('data/pacific_plant_label.csv', '0')

  
# scrape_pacific_plants_names()
# scrape_pacific_plants_location()
# scrape_pacific_plants_links()
# scrape_pacific_plants_data()
# clean_pacific_plants()
# scrape_invasive_plants()
# label_pacific_plants()