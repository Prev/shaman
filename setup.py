from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name = 'shamanld',
	long_description=long_description,
    long_description_content_type='text/markdown',
	packages = ['shamanld'],
	version = '1.1.0',
	description = 'Programming Language Detector',
	license = 'MIT',

	author = 'Youngsoo Lee',
	author_email = 'prevdev@gmail.com',
	
	url = 'https://github.com/Prev/shaman',
	keywords = ['language-detector', 'language', 'detector'],

	package_data={'shamanld': ['*.json.gz']},
	include_package_data=True,

	entry_points={
		'console_scripts': [
			'shaman-trainer = shamanld.trainer:main',
			'shaman-tester = shamanld.tester:main',
		],
	},
)
