from setuptools import setup
import os, stat

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='cifscloak',
    version='1.0.21',
    description='Mount cifs shares using encrypted passwords',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Darren Chambers',
    author_email='dazchambers@gmail.com',
    url='https://github.com/sudoofus/cifscloak',
    install_requires=[
	'cryptography',
	'argparse',
	'regex',
    ],

    scripts=['cifscloak.py'],
)
