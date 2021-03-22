[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Prev/shaman/blob/master/LICENSE)
[![Pypi](https://img.shields.io/pypi/v/shamanld.svg)](https://pypi.python.org/pypi/shamanld)
[![Build Status](https://travis-ci.org/Prev/shaman.svg)](https://travis-ci.org/Prev/shaman) 

# Shaman - Programming Language Detector

When you input `code`, Shaman detect its `language`.

Languages supported:
`ASP`, `Bash`, `C`, `C#`, `CSS`, `HTML`, `Java`, `JavaScript`,
`Objective-c`, `PHP`, `Python`, `Ruby`, `SQL`, `Swift`, and `XML`.

Shaman is implemented with Bayes Classification and pre-defined RegEx patterns.
Pre-trained model is included in the library, where the size of the model is **214KB**.

The accuracy of the included model is **78%** with the test set and 83% with the training set.
See accuracy section for detail.


## Getting Started

#### How to install

```bash
$ pip install shamanld
```

#### How to use

```python
from shamanld import Shaman

code = """
#include <stdio.h>
int main() {
    printf("Hello world");
}
"""

r = Shaman.default().detect(code)

print(r)
# [('c', 42.60959840702781), ('objective-c', 8.535893087527496), ('java', 7.237626324587697), ...]
```


## Test and train with your custom dataset

Shaman supports training the model with your custom dataset easily.
The only thing you have to prepare is to make your dataset with CSV format.
CSV file should include "language,code" pairs.

#### Test with custom dataset

```bash
$ shaman-tester path/to/test_set.csv
```

#### Training a new model with custom dataset

```bash
$ shaman-trainer path/to/training_set.csv --model-path path/to/your_model.json.gz
```

#### Testing custom model

```bash
$ shaman-trainer path/to/test_set.csv --model-path path/to/your_model.json.gz
```

#### Using custom model on the code
```python
from shamanld import Shaman

detector = Shaman('path/to/your_model.json.gz')
detector.detect('/* some code */')
```

## Test accuracy

Included model is trained with 120K codes and tested with 42K codes.
Only the codes whose lengths are more than 100 are used in both training & testing. As the codes are collected without verification, there might be some data with wrong labels.

| Language     | Accuracy                  |
|--------------|---------------------------|
| **Total**    | 78.40% (36428 / 46464)    |
| c            | 70.41% (11479 / 16304)    |
| java         | 90.24% (8094 / 8969)      |
| python       | 92.85% (5230 / 5633)      |
| javascript   | 63.08% (2782 / 4410)      |
| sql          | 80.92% (2519 / 3113)      |
| html         | 83.99% (2156 / 2567)      |
| c#           | 84.08% (1753 / 2085)      |
| xml          | 80.18% (635 / 792)        |
| bash         | 83.58% (560 / 670)        |
| swift        | 83.25% (522 / 627)        |
| php          | 73.09% (315 / 431)        |
| css          | 68.12% (203 / 298)        |
| objective-c  | 32.88% (121 / 368)        |
| asp          | 36.75% (43 / 117)         |
| ruby         | 20.00% (16 / 80)          |

## JavaScript version

JavaScript **inference** implementation is available at [Prev/shamanjs](https://github.com/Prev/shamanjs).

