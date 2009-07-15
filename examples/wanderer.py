#!/usr/bin/env python
# encoding: utf-8
"""
wanderer.py

Created by Paul Lamere on 2009-07-15
Copyright (c) 2009 The Echo Nest Corporation. All rights reserved.
"""

import sys
import os
import random

from pyechonest import artist, config

"""
Starting from an artist, build a playlist by wandering
around the artist neighborhood.
"""

usage = """
usage:
    python wander.py artist name
"""
# How to set your ECHO_NEST_API_KEY:
#   1) Set the environment variable 'ECHO_NEST_API_KEY' to be your key, or
#   2) Uncomment the next line and add your key between the quotes
#config.ECHO_NEST_API_KEY="YOUR API KEY HERE" 

def wander(band, max=15):
    count = 0
    while count < max:
        if band.audio():
            audio = random.choice(band.audio())
            play(audio)
            count += 1
        band = random.choice(band.similar())

def play(audio):
    if 'title' in audio and 'artist' in audio and 'url' in audio:
        print audio['title'],  "by", audio['artist'] 
        print "   ", audio['url']
        print


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        args = sys.argv[1:]
        name = ' '.join(args)
        alist = artist.search_artists(name)
        if (len(alist) > 0):
            wander(alist[0])
        else :
            print "Can't find ", name
    else:
        print usage
        sys.exit(-1)
