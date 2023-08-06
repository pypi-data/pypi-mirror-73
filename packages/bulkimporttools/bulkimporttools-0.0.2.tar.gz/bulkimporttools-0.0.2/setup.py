from setuptools import setup

with open("README.md","r") as fh:
	long_description = fh.read()

setup(
	name = 'bulkimporttools',
	version = '0.0.2',
	description = 'A collection of tools for importing classes and modules in bulk',
	py_modules = ["bulk_import"],
	package_dir = {'':'src'},
	classifiers = [
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
		"Operating System :: OS Independent",
		"Intended Audience :: Developers",
		"Development Status :: 1 - Planning",
	],
	url = "https://github.com/Mikael-MStinson/Bulk-Import",
	author = "Mikael Morrell-Stinson",
	long_description = long_description,
	long_description_content_type = "text/markdown",
)