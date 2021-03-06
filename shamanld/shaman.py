"""
Programming Language Detector

Usage
-------------------------------
from shamanld import Shaman
Shaman.default().detect(\"""
#include <stdio.h>
int main() {
    printf("Hello world");
}
\""")
# [('c', 44.54114006995534), ('java', 6.445867604204304), ('c#', 5.015724434781431), ...]

Model format
-------------------------------
{
    "version": "...",
    "languages": ["asp", "bash", "c", ...],
    "keywords": {
        "printf": [0, 0.001, 0.81321, ...],
        "...": [...],
    },
    "patterns": {
        "(<.+>[^<]*</.+>)|<\\?.+>": [0.131, 0.532, 0.512, ...],
        "...": [...],
    }
}

:author: Prev(prevdev@gmail.com)
:license: MIT
"""

import os
import json
import re
import math
import gzip


LANGUAGES_SUPPORTED = ('asp', 'bash', 'c', 'c#', 'css', 'html', 'java', 'javascript',
                       'objective-c', 'php', 'python', 'ruby', 'sql', 'swift', 'xml')
version = '1.1.0'


class Shaman:

    _default_instance = None

    @staticmethod
    def default():
        """ Get default shaman instance by "data/trained.json"
        """
        if Shaman._default_instance is not None:
            return Shaman._default_instance

        here = (os.path.dirname(__file__) or '.')
        Shaman._default_instance = Shaman(here + '/data/model.json.gz')
        return Shaman._default_instance

    def __init__(self, model_path):
        """ Shaman constructor
        """
        ext = model_path.split('.')[-1]
        if ext == 'json':
            with open(model_path) as file:
                self.model = json.loads(file.read())

        elif ext == 'gz':
            with gzip.open(model_path, 'rb') as f:
                self.model = json.loads(f.read().decode())

        else:
            raise Exception(
                'Unsupported file extension %s. Try using a model with .json or .json.gz file')

    def detect(self, code):
        """ Detect language with code
        """
        keywords = KeywordFetcher.fetch(code)
        probabilities = {}

        for keyword in keywords:
            if keyword not in self.model['keywords']:
                continue

            data = self.model['keywords'][keyword]
            # Average probability of all languages
            p_avg = sum(data) / len(data)

            for lang_id, probability in enumerate(data):
                # By Naïve Bayes Classification
                p = probability / p_avg

                # verbose language is defined in `languages` field of the model
                language = self.model['languages'][lang_id]
                probabilities[language] = probabilities.get(
                    language, 0) + math.log(1 + p)

        for pattern, data in self.model['patterns'].items():
            matcher = PatternMatcher(pattern)
            p0 = matcher.getratio(code)

            for lang_id, p_avg in enumerate(data):
                language = self.model['languages'][lang_id]
                if language not in probabilities:
                    continue

                p = 1 - abs(p_avg - p0)
                probabilities[language] *= p

        # Convert `log` operated probability to percentile
        sum_val = 0
        for language, p in probabilities.items():
            sum_val += math.pow(math.e / 2, p)

        for language, p in probabilities.items():
            probabilities[language] = math.pow(math.e / 2, p) / sum_val * 100

        return sorted(probabilities.items(), key=lambda a: a[1], reverse=True)


class KeywordFetcher:

    prog = re.compile('([a-zA-Z0-9$*#@_-]+)')

    @staticmethod
    def fetch(code):
        """ Fetch keywords by Code
        """
        ret = {}

        code = KeywordFetcher._remove_strings(code)
        result = KeywordFetcher.prog.findall(code)

        for keyword in result:
            if len(keyword) <= 1:
                # Ignore single-length word
                continue
            if len(keyword) >= 30:
                # Ignore too-long word
                continue
            if keyword.isdigit():
                # Ignore number
                continue

            # Remove first char if string is starting by '-' or '*' (Pointer or Negative numbers)
            if keyword[0] == '-' or keyword[0] == '*':
                keyword = keyword[1:]

            # Remove last char if string is finished by '-' or '*'
            if keyword[-1] == '-' or keyword[-1] == '*':
                keyword = keyword[0:-1]

            if len(keyword) <= 1:
                continue

            # `ret[ keyword ] += 1` with initial value
            ret[keyword] = ret.get(keyword, 0) + 1

        return ret

    @staticmethod
    def _remove_strings(code):
        """ Remove strings in code
        """
        removed_string = ""
        is_string_now = None

        for i in range(0, len(code)-1):
            append_this_turn = False

            if code[i] == "'" and (i == 0 or code[i-1] != '\\'):
                if is_string_now == "'":
                    is_string_now = None

                elif is_string_now is None:
                    is_string_now = "'"
                    append_this_turn = True

            elif code[i] == '"' and (i == 0 or code[i-1] != '\\'):
                if is_string_now == '"':
                    is_string_now = None

                elif is_string_now is None:
                    is_string_now = '"'
                    append_this_turn = True

            if is_string_now is None or append_this_turn:
                removed_string += code[i]

        return removed_string


class PatternMatcher:

    PATTERNS = [
        r'(<.+>[^<]*</.+>)|<\\?.+>',  # markup
        r'([a-zA-Z0-9-_]+)\s*:\s*.*\s*;',  # css
        r'def\s+([^(]+)\s*\([^)]*\)\s*:',  # python
        r'function\s+\([^)]*\)\s*{[^}]*}',  # js-style function
        r'var\s+[a-zA-Z0-9_$]+',  # js-style var
        r'\$[a-zA-Z0-9_$]+',  # sigil style var
        r'\([^)]*\)\s*{[^}]*}',  # c-style block
    ]

    def __init__(self, pattern):
        """ Pattern Matcher Constructor
        :param pattern: regex pattern string
        """
        self.prog = re.compile(pattern)

    def getratio(self, code):
        """ Get ratio of code and pattern matched
        """
        if code == '':
            return 0

        code_replaced = self.prog.sub('', code)
        return (len(code) - len(code_replaced)) / len(code)
