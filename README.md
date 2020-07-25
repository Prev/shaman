# Shaman
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ratchetcloud/powerforums/blob/master/LICENSE)
[![Pypi](https://img.shields.io/pypi/v/shamanld.svg)](https://pypi.python.org/pypi/shamanld)
[![Build Status](https://travis-ci.org/Prev/shaman.svg)](https://travis-ci.org/Prev/shaman) 

Programming Language Detector  
When you input `code`, Shaman detect its `language`.

## Install

```bash
$ pip install shamanld
```

## Usage

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
# [('c', 44.54114006995534), ('java', 6.445867604204304), ('c#', 5.015724434781431), ...]
```

## Languages supported

ASP, Bash, C, C#, CSS, , HTML, Java, JavaScript, JSP,
Objective-c, PHP, Python, Ruby, SQL, Swift, and XML.


## Accuracy

~80%  

<img src="https://raw.githubusercontent.com/Prev/shaman/master/resources/accuracy.png" width="500" alt="Accuracy">

## Test shaman using CLI

#### Test single file

```bash
$ shaman-tester -f sample1.cpp
c: 99.98%
c#: 0.02%
java: 0.00%
javascript: 0.00%
```

#### Test bunch of code
```bash
$ shaman-tester -b codes.csv
# CSV format: language, code
```


## Using custom trained set

#### Make custom trained set
```bash
$ shaman-trainer code_bunch.csv custom_trained_set.json
# CSV format: language, code
```

#### Use custom trained set
```python
from shamanld import Shaman

detector = Shaman(open('custom_trained_set.json'))
detector.detect('some code')
```

## JavaScript version

JavaScript **inferencing** implementation is available at [Prev/shamanjs](https://github.com/Prev/shamanjs). (Note: training is not available in JS version)


