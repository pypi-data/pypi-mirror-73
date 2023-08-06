from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name = 'onlyocr',
	version = '1.0.0',
	author = 'Devaloy Mukherjee',
	author_email = 'devaloy.mukherjee@gmail.com',
	long_description=long_description,
    long_description_content_type="text/markdown",
	packages = find_packages()
	)
