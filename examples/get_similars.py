#!/usr/bin/env python
# encoding: utf-8
"""
get_similars.py

Created by Paul Lamere on 2009-06-29.
Copyright (c) 2009 The Echo Nest Corporation. All rights reserved.
"""

import sys
import os
from pyechonest import artist, config

"""
find similar artists for the given artist.
"""

usage = """
usage:
    python get_similars.py artist name
"""
# How to set your ECHO_NEST_API_KEY:
#   1) Set the environment variable 'ECHO_NEST_API_KEY' to be your key, or
#   2) Uncomment the next line and add your key between the quotes
#config.ECHO_NEST_API_KEY="YOUR API KEY HERE" 

def main(artist_name):	
    alist = artist.search_artists(artist_name)
    if (len(alist) > 0):
        print 'Artists similar to', alist[0].name
        for sim in alist[0].similar():
            print " ", sim.name
    else :
        print "Can't find ", artist_name

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        args = sys.argv[1:]
        name = ' '.join(args)
        main(name)
    else:
        print usage
        sys.exit(-1)
