"""
Train Shaman with CSV file ("language, code" foramt)

Usage:
	python trainer.py <test_set.csv> [--model-path <output_model_path>] [--light]

:author: Prev(prevdev@gmail.com)
:license: MIT
"""
import shaman
import argparse
import sys
import os
import csv
import json
import gzip

def main() :
	aparser = argparse.ArgumentParser()
	aparser.add_argument('path', type=str, help='Path of the CSV file for training ("language, code" foramt)')
	aparser.add_argument('--model-path', type=str, help='Output path of the trained model file', default='model.json.gz')
	aparser.add_argument('--light', type=bool, help='Make light-weighted model file', default=False, const=True, nargs='?')
	args = aparser.parse_args()

	if not os.path.isfile(args.path):
		print('"%s" is not a file' % args.path)
		sys.exit(-1)

	csv.field_size_limit(sys.maxsize) # Set CSV limit to sys.maxsize
	filedata = []

	print('Load CSV file')
	with open(args.path) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader :
			filedata.append(row)

	min_keyword_num = 20
	if args.light:
		min_keyword_num = 40

	# Fetch keyword data
	trained_data = {}
	trained_data['keywords'] = fetch_keywords(filedata, min_keyword_num)
	trained_data['patterns'] = match_patterns(filedata)

	# Save result
	with gzip.open(args.model_path, 'wb') as f:
		f.write(json.dumps(trained_data).encode())

	print('Trained model is saved at "%s"' % args.model_path)


def fetch_keywords(codedata, min_keyword_num = 20) :
	""" Fetch keywords by shaman.KeywordFetcher
		Get average probabilities of keyword and language
	"""
	lang_cnt = {}
	lk_cnt = {} # [language][keyword] = count
	# Read row in codedata and count keywords in codes with langauge
	for index, (language, code) in enumerate(codedata):
		if language not in shaman.LANGUAGES_SUPPORTED:
			continue

		if language not in lk_cnt:
			lk_cnt[language] = {}
			lang_cnt[language] = 0

		lang_cnt[language] += 1

		for keyword in shaman.KeywordFetcher.fetch( code ):
			# if keyword exists in fetched data, add '1' to keyword data
			lk_cnt[language][keyword] = lk_cnt[language].get(keyword, 0) + 1

		print('Fetch keyword %d/%d    ' % (index, len(codedata)), end='\r')

	# Get dataset indexed by keyword
	ret = {}
	for language in lk_cnt:
		for keyword, count in lk_cnt[language].items() :
			if keyword not in ret :
				ret[keyword] = {}

			ret[keyword][language] = (count / lang_cnt[ language ]) # Probability
			ret[keyword]['$$total'] = ret[keyword].get('$$total', 0) + count


	# Check total counts of the keyword and ignore if count is too small
	# (threshold is determined by `min_keyword_num`)
	keywords2remove = []

	for keyword in ret:
		if ret[keyword]['$$total'] < min_keyword_num:
			keywords2remove.append(keyword)
			continue
		del ret[keyword]['$$total']

	for keyword in keywords2remove:
		del ret[keyword]

	print('Fetch keyword completed        ')
	return ret


def match_patterns(codedata) :
	""" Match patterns by shaman.PatternMatcher
		Get average ratio of pattern and language
	"""

	ret = {}

	for index1, pattern in enumerate(shaman.PatternMatcher.PATTERNS):
		print('Matching pattern %d "%s"' % (index1+1, pattern))

		matcher = shaman.PatternMatcher(pattern)
		tmp = {}

		for index2, (language, code) in enumerate(codedata):
			if language not in shaman.LANGUAGES_SUPPORTED:
				continue
			if len(code) <= 20 or len(code) > 100000:
				continue

			if language not in tmp:
				tmp[language] = []

			ratio = matcher.getratio(code)
			tmp[language].append(ratio)

			print('Matching patterns %d/%d    ' % (index2, len(codedata)), end='\r')

		ret[pattern] = {}
		for language, data in tmp.items():
			ret[pattern][language] = sum(tmp[language]) / max(len(tmp[language]), 1)

	print('Matching patterns completed          ')
	return ret

if __name__ == '__main__':
	main(args)
