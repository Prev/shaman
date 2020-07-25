from setuptools import setup


setup(
	name = 'shamanld',
	packages = ['shamanld'],
	version = '1.0.0',
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