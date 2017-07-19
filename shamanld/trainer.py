"""
	shaman/trainer
	-----------------
	Train shaman by code bunch

	Usage: 
		python trainer.py <code_bunch.csv> <result.json>

	:author: Prev(prevdev@gmail.com)
	:license: MIT
"""

from . import shaman
import sys, os
import csv, json


def run() :
	if len(sys.argv) != 3 :
		# Exception handling on starting program
		print('Usage: "shaman-trainer <code_bunch.csv> <result.json>"')
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


	# Fetch keyword data
	trained_data = {}
	trained_data['keywords'] = fetch_keywords(filedata)
	trained_data['patterns'] = match_patterns(filedata)

	# Save result
	with open(result_file, 'w') as file :
		file.write( json.dumps(trained_data) )

	print('Trained result is saved at "%s"' % result_file)


def fetch_keywords(codedata) :
	""" Fetch keywords by shaman.KeywordFetcher
		Get average probabilities of keyword and language
	"""

	# Read row in codedata and count keywords in codes with langauge
	tmp = {}
	language_counts = {}

	for index, (language, code) in enumerate(codedata) :
		if language not in shaman.SUPPORTING_LANGUAGES :
			continue

		if language not in tmp :
			tmp[language] = {}
			language_counts[language] = 0

		language_counts[language] += 1

		for keyword in shaman.KeywordFetcher.fetch( code ) :
			# if keyword exists in fetched data, add '1' to keyword data
			tmp[language][keyword] = tmp[language].get(keyword, 0) + 1

		print('Fetch keyword %d/%d    ' % (index, len(codedata)), end='\r')


	# Get dataset indexed by keyword
	ret = {}

	for language in tmp :
		for keyword, count in tmp[ language ].items() :	
			if keyword not in ret :
				ret[ keyword ] = {}

			ret[ keyword ][ language ] = (count / language_counts[ language ]) # Probability

	print('Fetch keyword completed        ')
	return ret



def match_patterns(codedata) :
	""" Match patterns by shaman.PatternMatcher
		Get average ratio of pattern and language
	"""

	ret = {}

	for index1, pattern in enumerate(shaman.PatternMatcher.PATTERNS) :
		print('Matching pattern %d "%s"' % (index1+1, pattern))

		matcher = shaman.PatternMatcher(pattern)
		tmp = {}

		for index2, (language, code) in enumerate(codedata) :
			if language not in shaman.SUPPORTING_LANGUAGES :
				continue

			if len(code) <= 20 or len(code) > 100000 :
				continue

			if language not in tmp :
				tmp[language] = []

			ratio = matcher.getratio(code)
			tmp[language].append(ratio)

			print('Matching patterns %d/%d    ' % (index2, len(codedata)), end='\r')


		ret[pattern] = {}
		for language, data in tmp.items() :
			ret[pattern][language] = sum(tmp[language]) / max(len(tmp[language]), 1)

	print('Matching patterns completed          ')
	return ret

run()
