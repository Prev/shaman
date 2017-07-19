"""
	shaman/tester
	-----------------
	Test shaman
	
	Usage: 
		python tester.py --help
		python tester.py --test <code_bunch.csv> : Test with code bunch (with answer set)
		python tester.py --file <somecode.java> : Test with single file

	:author: Prev(prevdev@gmail.com)
	:license: MIT
"""

from . import shaman
import sys, os
import csv, json
import argparse


aparser = argparse.ArgumentParser()
aparser.add_argument("-b", "--bunch", help="Test with code bunch (with answer set)")
aparser.add_argument("-f", "--file", help="Test with single file")
args = aparser.parse_args()


def run() :
	if args.file:
		test_with_file(args.file)

	elif args.bunch:
		test_with_bunch(args.bunch)

	else:
		print('to see help, COMMAND "shaman-tester --help"')
		sys.exit()



def test_with_file(filename) :
	""" Detect langauge with single files
		Print top 3 languages by calculated probabilities
	"""
	if not os.path.exists(filename) :
		print('File not exists: ' + filename)
		sys.exit(-1)

	with open(filename, 'r') as file :
		code = file.read()

	probabilities = shaman.Shaman.default().detect( code )
	
	for index, (lang, prob) in enumerate(probabilities) :
		if index > 3: break
		
		print("%s: %.2lf%%" % (lang, prob))


def test_with_bunch(filename) :
	""" Test shaman with code bunch and show statistics
	"""

	if not os.path.exists(filename) :
		print('File not exists: ' + filename)
		sys.exit(-1)


	# Read CSV file
	print('Load CSV file')

	csv.field_size_limit(sys.maxsize) # Set CSV limit to sys.maxsize
	filedata = []
	with open(filename) as csvfile :
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader :
			filedata.append(row)


	detector = shaman.Shaman.default()

	correct = 0
	totals = len(filedata)

	results = {}
	print('Start testing')

	for index, (language, code) in enumerate(filedata) :
		print ('Testing %s/%s     ' % (index, len(filedata)), end="\r")

		if language not in shaman.SUPPORTING_LANGUAGES:
			totals -= 1
			continue

		try :
			glang = detector.detect( code )[0][0]
		except IndexError :
			glang = None

		if language not in results :
			results[ language ] = [0, 0, 0]

		if glang == language :
			correct += 1
			results[ language ][0] += 1

		
		results[ language ][1] += 1
		results[ language ][2] = results[ language ][0] / results[ language ][1]


	
	print("------------------------------------------------")
	print("Accuracy: %.2lf%% (Correct: %d / Valid Data: %d)" % (correct/totals*100, correct, totals))
	print("------------------------------------------------")
	
	results = sorted(results.items(), key=lambda x: x[1][0], reverse=True)
	for lang, l in results :
		print("%s: %.2lf%% (%s/%s)" % (lang, l[2] * 100, l[0], l[1]))

run()
