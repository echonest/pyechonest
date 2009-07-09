#!/usr/bin/env python

__version__ = "$Revision: 0 $"
# $Source$

from distutils.core import setup

setup(name='pyechonest',
      version='1.0',
      description='Python interface to The Echo Nest web APIs.',
      author='Ben Lacker',
      author_email='ben@echonest.com',
      maintainer='Ben Lacker',
      maintainer_email='ben@echonest.com',
      url='http://code.google.com/p/pyechonest/',
      download_url='http://code.google.com/',
      package_dir={'pyechonest':'src/pyechonest'},
      packages=['pyechonest'],
      requires=['math',
                'urllib'
                ]
     )
