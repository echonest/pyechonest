#!/usr/bin/env python
# encoding: utf-8
"""
tutorial1.py

Created by Paul Lamere on 2010-03-25.
Copyright (c) 2010 The Echo Nest Corporation. All rights reserved.
"""

import sys
import os
from pyechonest import artist, config

"""
Prints the name hotttness and familiarity of the 25 top hottttest artists
"""

usage = """
usage:
    python tutorial1.py 
"""
# How to set your ECHO_NEST_API_KEY:
#   1) Set the environment variable 'ECHO_NEST_API_KEY' to be your key, or
#   2) Uncomment the next line and add your key between the quotes
#config.ECHO_NEST_API_KEY="YOUR API KEY HERE" 

def main():	
    artists = artist.get_top_hottt_artists(rows=25)
    for a in artists:
        print "%.2f %.2f %s" % (a.hotttnesss(), a.familiarity(), a.name)

if __name__ == '__main__':
    main()
