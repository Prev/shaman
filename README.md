# Shaman
[![Pypi](https://img.shields.io/pypi/v/shamanld.svg)](https://pypi.python.org/pypi/shamanld)
[![Build Status](https://travis-ci.org/Prev/shaman.svg)](https://travis-ci.org/Prev/shaman) 

Programming Language Detector


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
```

## Test single file
```bash
$ shaman-tester -f sample1.cpp
```

## Test bunch of files
```bash
$ shaman-tester -b codes.csv
# CSV format: language, code
```

## Make custom trained set
```bash
$ shaman-trainer code_bunch.csv custom_trained_set.json
# CSV format: language, code
```

## Use custom trained set
```python
from shamanld import Shaman

detector = Shaman(open('custom_trained_set.json'))
detector.detect('some code')

```