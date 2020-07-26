"""
Accuracy tester of Shaman

Usage:
	shaman-tester <test_set.csv> [--model-path <model_path>]

:author: Prev(prevdev@gmail.com)
:license: MIT
"""

from . import shaman
import sys, os
import csv, json
import argparse

def main() :
	aparser = argparse.ArgumentParser()
	aparser.add_argument('path', type=str, help='Path of the CSV file to test accuracy of Shaman ("language, code" foramt)')
	aparser.add_argument('--model-path', type=str, help='Model file path to use', default=None)
	args = aparser.parse_args()

	if not os.path.exists(args.path) :
		print('File not exists: ' + args.path)
		sys.exit(-1)

	if args.model_path:
		print('Use model on %s' % args.model_path)
		detector = shaman.Shaman(args.model_path)
	else:
		detector = shaman.Shaman.default()
	test_with_bunch(args.path, detector)

def test_with_bunch(filepath, detector) :
	""" Test shaman with code bunch and show statistics
	"""
	print('Load CSV file')

	csv.field_size_limit(sys.maxsize) # Set CSV limit to sys.maxsize
	filedata = []
	with open(filepath) as csvfile :
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader :
			filedata.append(row)

	correct = 0
	totals = len(filedata)

	results = {}
	print('Start testing')

	for index, (language, code) in enumerate(filedata) :
		print ('Testing %s/%s     ' % (index, len(filedata)), end="\r")

		if language not in shaman.LANGUAGES_SUPPORTED:
			totals -= 1
			continue
		if language not in results:
			results[language] = [0, 0, 0]

		try :
			inferenced = detector.detect(code)[0][0]
		except IndexError :
			inferenced = None

		if inferenced == language :
			correct += 1
			results[ language ][0] += 1

		results[language][1] += 1
		results[language][2] = results[language][0] / results[language][1]

	print('------------------------------------------------')
	print('Accuracy: %.2lf%% (%d / %d)' % (correct/totals*100, correct, totals))
	print('------------------------------------------------')

	results = sorted(results.items(), key=lambda x: x[1][0], reverse=True)
	for lang, l in results :
		print('%s: %.2lf%% (%s/%s)' % (lang, l[2] * 100, l[0], l[1]))

if __name__ == '__main__':
	main(args)
