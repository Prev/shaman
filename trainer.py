"""
	shaman/trainer
	-----------------
	Train shaman by code bunch

	Usage: 
		python trainer.py <code_bunch.csv> <result.json>

	:author: Prev(prevdev@gmail.com)
	:license: MIT
"""

import shaman
import sys, os
import csv, json

if len(sys.argv) != 3 :
	# Exception handling on starting program
	print('Usage: "python trainer.py <code_bunch.csv> <result.json>"')
	sys.exit(-1)


# Args
codebunch_file = sys.argv[1]
result_file = sys.argv[2]


if not os.path.isfile(codebunch_file) :
	# Exception handling of <code bunch> file
	print('"%s" is not a file' % codebunch_file)
	sys.exit(-1)



# Read CSV file
csv.field_size_limit(sys.maxsize) # Set CSV limit to sys.maxsize
filedata = []

print('Load CSV file')

with open(codebunch_file) as csvfile :
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader :
		filedata.append(row)



# Read row in filedata and count keywords in codes with langauge
keyword_data = {}
language_counts = {}

for index, row in enumerate(filedata) :
	language, code = row

	if language not in shaman.SUPPORTING_LANGUAGES :
		continue

	if language not in keyword_data :
		keyword_data[language] = {}
		language_counts[language] = 0

	language_counts[language] += 1

	for keyword in shaman.KeywordFetcher.fetch( code ) :
		# if keyword exists in fetched data, add '1' to keyword data
		keyword_data[language][keyword] = keyword_data[language].get(keyword, 0) + 1

	print ('Fetch keyword %d/%d    ' % (index, len(filedata)), end='\r')

print('Fetch keyword completed')



# Get dataset indexed by keyword
calced_data = {}

for language in keyword_data :
	for keyword, count in keyword_data[ language ].items() :	
		if keyword not in calced_data :
			calced_data[ keyword ] = {}

		calced_data[ keyword ][ language ] = (count / language_counts[ language ]) # Probability



# Save result
with open(result_file, 'w') as file :
	file.write( json.dumps(calced_data) )

print('Trained result is saved at "%s"' % result_file)
