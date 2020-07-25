from shamanld import Shaman

def test_detection1() :
	code = """#include <stdio.h>
	int main() {
		printf("Hello world");
	}
	"""

	r = Shaman.default().detect(code)
	assert r[0][0] == 'c'

def test_detection2() :
	code = """<!doctype>
	<html>
		<head></head>
		<body>Hello world</head>
	</html>
	"""

	r = Shaman.default().detect(code)
	assert r[0][0] == 'html'
