[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ratchetcloud/powerforums/blob/master/LICENSE)
[![Pypi](https://img.shields.io/pypi/v/shamanld.svg)](https://pypi.python.org/pypi/shamanld)
[![Build Status](https://travis-ci.org/Prev/shaman.svg)](https://travis-ci.org/Prev/shaman) 

# Shaman - Programming Language Detector

When you input `code`, Shaman detect its `language`.

Languages supported:
`ASP`, `Bash`, `C`, `C#`, `CSS`, `HTML`, `Java`, `JavaScript`, `JSP`,
`Objective-c`, `PHP`, `Python`, `Ruby`, `SQL`, `Swift`, and `XML`.

Implemented base on Naïve Bayes Classification and pre-defined pattern matching.
Pre-trained model is included in the library, where the size of the model is only **248KB**.

The accuracy of the included model is about 75% with the test set and 80% with the training set.
I trained the model with 100K codes and tested with 40K codes.


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
# [('c', 38.27568605456699), ('objective-c', 8.802419110662512), ('java', 7.5835661834984585), ...]
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
$ shaman-trainer path/to/training_set.csv path/to/your_model.json.gz
```

#### Testing custom model

```bash
$ shaman-trainer path/to/test_set.csv path/to/your_model.json.gz
```

#### Using custom model on the code
```python
from shamanld import Shaman

detector = Shaman('path/to/your_model.json.gz')
detector.detect('/* some code */')
```

## JavaScript version

JavaScript **inferencing** implementation is available at [Prev/shamanjs](https://github.com/Prev/shamanjs). (Note: training is not available in JS version)


