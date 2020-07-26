[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Prev/shaman/blob/master/LICENSE)
[![Pypi](https://img.shields.io/pypi/v/shamanld.svg)](https://pypi.python.org/pypi/shamanld)
[![Build Status](https://travis-ci.org/Prev/shaman.svg)](https://travis-ci.org/Prev/shaman) 

# Shaman - Programming Language Detector

When you input `code`, Shaman detect its `language`.

Languages supported:
`ASP`, `Bash`, `C`, `C#`, `CSS`, `HTML`, `Java`, `JavaScript`, `JSP`,
`Objective-c`, `PHP`, `Python`, `Ruby`, `SQL`, `Swift`, and `XML`.

Shaman is implemented base on Naïve Bayes Classification and pattern matching technique.
Pre-trained model is included in the library, where the size of the model is only **167KB**.

The accuracy of the included model is about **75%** with the test set and 80% with the training set.
The model is trained with 100K codes and tested with 40K codes.


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
CSV file should includes "language,code" pairs.

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

## JavaScript version

JavaScript **inferencing** implementation is available at [Prev/shamanjs](https://github.com/Prev/shamanjs).

