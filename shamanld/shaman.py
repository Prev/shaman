"""
	shaman/shaman
	-----------------
	Programming Language Detector

	:author: Prev(prevdev@gmail.com)
	:license: MIT
"""

SUPPORTING_LANGUAGES = ('actionscript', 'asp', 'bash', 'c', 'c#', 'css', 'haxe', 'html', 'java', 'javascript', 'jsp', 'objective-c', 'perl', 'php', 'python', 'ruby', 'sql', 'swift', 'visualbasic', 'xml')

import os, json
import re
import math

class Shaman :

	_default_instance = None

	@staticmethod
	def default() :
		""" Get default shaman instance by "data/trained.json"
		"""
		if Shaman._default_instance is not None :
			return Shaman._default_instance

		with open((os.path.dirname(__file__) or '.') + '/data/trained.json') as file :
			tset = json.loads(file.read())

		Shaman._default_instance = Shaman(tset)
		return Shaman._default_instance


	def __init__(self, trained_set) :
		""" Shaman constructor
		"""
		if hasattr(trained_set, 'read') :
			trained_set = json.loads(trained_set.read())

		self.trained_set = trained_set


	def detect(self, code) :
		""" Detect language with code
		"""
		
		keywords = KeywordFetcher.fetch( code )
		probabilities = {}

		for keyword in keywords :
			if keyword not in self.trained_set['keywords'] :
				continue

			data = self.trained_set['keywords'][keyword]
			p_avg = sum(data.values()) / len(data) # Average probability of all languages

			for language, probability in data.items() :
				# By Naïve Bayes Classification
				p = probability / p_avg

				probabilities[ language ] = probabilities.get(language, 0) + math.log(1 + p)



		for pattern, data in self.trained_set['patterns'].items() :
			# print('pattern ("%s")' % pattern)

			matcher = PatternMatcher(pattern)
			p0 = matcher.getratio(code)
			# print(p0)

			for language, p_avg in data.items() :
				if language not in probabilities :
					continue

				p = 1 - abs(p_avg - p0)
				probabilities[ language ] *= p
				
				# print('%s: %s' % (language, p_avg))

			# print('---------')


		# Convert `log` operated probability to percentile
		sum_val = 0
		for language, p in probabilities.items() :
			sum_val += math.pow(math.e / 2, p)

		for language, p in probabilities.items() :
			probabilities[language] = math.pow(math.e / 2, p) / sum_val * 100

		return sorted(probabilities.items(), key=lambda a: a[1], reverse=True)




class KeywordFetcher :
	
	prog = re.compile('([a-zA-Z0-9$*#@_-]+)')

	@staticmethod
	def fetch(code) :
		""" Fetch keywords by Code
		"""
		ret = {}

		code = KeywordFetcher._remove_strings(code)
		result = KeywordFetcher.prog.findall(code)

		for keyword in result :
			if len(keyword) <= 1: continue # Ignore single-length word
			if keyword.isdigit(): continue # Ignore number

			if keyword[0] == '-' or keyword[0] == '*' : keyword = keyword[1:] # Remove first char if string is starting by '-' or '*' (Pointer or Negative numbers)
			if keyword[-1] == '-' or keyword[-1] == '*' : keyword = keyword[0:-1] # Remove last char if string is finished by '-' or '*'

			if len(keyword) <= 1: continue

			ret[ keyword ] = ret.get(keyword, 0) + 1 # `ret[ keyword ] += 1` with initial value

		return ret


	@staticmethod
	def _remove_strings(code) :
		""" Remove strings in code
		"""
		removed_string = ""
		is_string_now = None
		
		for i in range(0, len(code)-1) :
			append_this_turn = False

			if code[i] == "'" and (i == 0 or code[i-1] != '\\') :
				if is_string_now == "'" :
					is_string_now = None

				elif is_string_now == None :
					is_string_now = "'"
					append_this_turn = True

			elif code[i] == '"' and (i == 0 or code[i-1] != '\\') :
				if is_string_now == '"' :
					is_string_now = None

				elif is_string_now == None :
					is_string_now = '"'
					append_this_turn = True


			if is_string_now == None or append_this_turn == True :
				removed_string += code[i]

		return removed_string



class PatternMatcher :

	PATTERNS = [
		r'(<.+>[^<]*<\/.+>)|<\\?.+>', #markup
		r'([a-zA-Z0-9-_]+)\s*:\s*.*\s*;', #css
		r'def\s+([^(]+)\s*\([^)]*\)\s*:', #python
		r'function\s+\([^)]*\)\s*{[^}]*}', #js-style function
		r'var\s+[a-zA-Z0-9_$]+', #js-style var
		r'\$[a-zA-Z0-9_$]+', #sigil style var
		r'\([^)]*\)\s*{[^}]*}', # c-style block
	]

	def __init__(self, pattern) :
		""" Pattern Matcher Constructor
		:param pattern: regex pattern string
		"""
		self.prog = re.compile(pattern)


	def getratio(self, code) :
		""" Get ratio of code and pattern matched
		"""
		if len(code) == 0 : return 0

		code_replaced = self.prog.sub('', code)
		return (len(code) - len(code_replaced)) / len(code)
	
