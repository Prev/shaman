"""
Train Shaman with CSV file ("language, code" foramt)

Usage:
    shaman-trainer <trainer_set.csv> [--model-path <output_model_path>] [--light]
    python -m shamanld.trainer <trainer_set.csv> [--model-path <output_model_path>] [--light]

Model format:
{
    "version": "...",
    "languages": ["asp", "bash", "c", ...],
    "keywords": {
        "printf": [0, 0.001, 0.81321, ...],
        "...": [...],
    },
    "patterns": {
        "(<.+>[^<]*<\\/.+>)|<\\?.+>": [0.131, 0.532, 0.512, ...],
        "...": [...],
    }
}

:author: Prev(prevdev@gmail.com)
:license: MIT
"""

import argparse
import sys
import os
import csv
import json
import gzip

from . import shaman


def main():
    aparser = argparse.ArgumentParser()
    aparser.add_argument(
        'path', type=str, help='Path of the CSV file for training ("language, code" foramt)')
    aparser.add_argument('--model-path', type=str,
                         help='Output path of the trained model file', default='model.json.gz')
    aparser.add_argument('--light', type=bool, help='Make light-weighted model file',
                         default=False, const=True, nargs='?')
    args = aparser.parse_args()

    if not os.path.isfile(args.path):
        print('"%s" is not a file' % args.path)
        sys.exit(-1)

    # Convert verbose language to unique number
    lang2index = {}
    for i, language in enumerate(shaman.LANGUAGES_SUPPORTED):
        lang2index[language] = i

    # Set CSV limit to sys.maxsize
    csv.field_size_limit(sys.maxsize)
    training_data = []

    print('Load CSV file')
    with open(args.path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for (language, code) in reader:
            if language not in lang2index:
                continue

            training_data.append((lang2index[language], code))

    num_languages = len(shaman.LANGUAGES_SUPPORTED)

    # Fetch keyword data
    model = {}
    model['version'] = shaman.version
    model['languages'] = shaman.LANGUAGES_SUPPORTED
    model['keywords'] = fetch_keywords(
        training_data, num_languages, 40 if args.light else 20)
    model['patterns'] = match_patterns(training_data, num_languages)

    # Compress model by dropping float precision
    print('Compress model')
    _drop_float_precision(model['keywords'], 7)
    _drop_float_precision(model['patterns'], 7)

    # Save result
    with gzip.open(args.model_path, 'wb') as f:
        f.write(json.dumps(model, separators=(',', ':')).encode())

    print('Trained model is saved at "%s"' % args.model_path)


def fetch_keywords(training_data, num_languages, min_keyword_num=20):
    """ Fetch keywords by shaman.KeywordFetcher
            Get average probabilities of keyword and language
    """
    cnt_per_lang = [0] * num_languages
    cnt_per_lang_kw = [{} for _ in range(num_languages)]

    # Read row in training_data and count keywords in codes with langauge
    for index, (lang_id, code) in enumerate(training_data):
        cnt_per_lang[lang_id] += 1

        for keyword in shaman.KeywordFetcher.fetch(code):
            # if keyword exists in fetched data, add '1' to keyword data
            cnt_per_lang_kw[lang_id][keyword] = cnt_per_lang_kw[lang_id].get(
                keyword, 0) + 1

        print('Fetch keyword %d/%d    ' %
              (index, len(training_data)), end='\r')

    # Get dataset indexed by keyword
    ret = {}
    keyword_cnt = {}
    for lang_id, obj in enumerate(cnt_per_lang_kw):
        for keyword, count in obj.items():
            if keyword not in ret:
                ret[keyword] = [0] * num_languages

            # Record probability
            ret[keyword][lang_id] = (count / cnt_per_lang[lang_id])

            # Record total count of this keyword
            keyword_cnt[keyword] = keyword_cnt.get(keyword, 0) + count

    # Check total counts of the keyword and ignore if count is too small
    # (threshold is determined by `min_keyword_num`)
    keywords2remove = []
    for keyword in ret:
        if keyword_cnt[keyword] < min_keyword_num:
            keywords2remove.append(keyword)
            continue
        del keyword_cnt[keyword]

    for keyword in keywords2remove:
        del ret[keyword]

    print('Fetch keyword completed        ')
    return ret


def match_patterns(training_data, num_languages):
    """ Match patterns by shaman.PatternMatcher
            Get average ratio of pattern and language
    """

    ret = {}

    for index1, pattern in enumerate(shaman.PatternMatcher.PATTERNS):
        print('Matching pattern %d "%s"' % (index1+1, pattern))

        matcher = shaman.PatternMatcher(pattern)
        ratios_per_lang = [[] for _ in range(num_languages)]

        for index2, (lang_id, code) in enumerate(training_data):
            if len(code) <= 20 or len(code) > 100000:
                continue

            ratio = matcher.getratio(code)
            ratios_per_lang[lang_id].append(ratio)

            print('Matching patterns %d/%d    ' %
                  (index2, len(training_data)), end='\r')

        ret[pattern] = [[] for _ in range(num_languages)]
        for lang_id, ratio_list in enumerate(ratios_per_lang):
            ret[pattern][lang_id] = sum(ratio_list) / max(len(ratio_list), 1)

    print('Matching patterns completed          ')
    return ret


def _drop_float_precision(dict_obj, point):
    """Drop float precsion for reducing the size of the model
    """
    for keyword in dict_obj.keys():
        for lang_id, prob in enumerate(dict_obj[keyword]):
            dict_obj[keyword][lang_id] = round(prob, point)


if __name__ == '__main__':
    main()
