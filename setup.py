from setuptools import setup


setup(
	name = 'shamanld',
	packages = ['shamanld'],
	version = '0.12',
	description = 'Programming Language Detector',
	license = 'MIT',

	author = 'Youngsoo Lee',
	author_email = 'prevdev@gmail.com',
	
	url = 'https://github.com/Prev/shaman',
	keywords = ['language-detector', 'language', 'detector'],

	package_data={'shamanld': ['*.json']},
	include_package_data=True,

	entry_points={
		'console_scripts': [
			'shaman-trainer = shamanld.trainer:run',
			'shaman-tester = shamanld.tester:run',
		],
	},
)