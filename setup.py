#!/usr/bin/env python
# encoding: utf-8

__version__ = "4.2.21"

# $Source$
from sys import version
import os
from setuptools import setup

if version < '2.6':
    requires=['urllib', 'urllib2', 'simplejson']
elif version >= '2.6':
    requires=['urllib', 'urllib2', 'json']
else:
    #unknown version?
    requires=['urllib', 'urllib2']

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pyechonest',
    version=__version__,
    description='Python interface to The Echo Nest APIs.',
    long_description=read('README.md'),
    author='Tyler Williams',
    author_email='tyler@echonest.com',
    maintainer='Tyler Williams',
    maintainer_email='tyler@echonest.com',
    url='https://github.com/echonest/pyechonest',
    download_url='https://github.com/echonest/pyechonest',
    package_dir={'pyechonest':'pyechonest'},
    packages=['pyechonest'],
    requires=requires
)
