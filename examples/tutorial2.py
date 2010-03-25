#!/usr/bin/env python
# encoding: utf-8
"""
tutorial2.py

Created by Paul Lamere on 2010-03-25.
Copyright (c) 2010 The Echo Nest Corporation. All rights reserved.
"""

import sys
import os
from pyechonest import artist, config

"""
Shows recent blog posts and audio for the hotttest artist
"""

usage = """
usage:
    python tutorial2.py 
"""
# How to set your ECHO_NEST_API_KEY:
#   1) Set the environment variable 'ECHO_NEST_API_KEY' to be your key, or
#   2) Uncomment the next line and add your key between the quotes
#config.ECHO_NEST_API_KEY="YOUR API KEY HERE" 

def main():	
    top_hot = artist.get_top_hottt_artists(rows=1)[0]
    print top_hot.name, top_hot.identifier
    print 'Audio for ', top_hot.name
    for audio in top_hot.audio(rows=5):
        print '   ', audio['title']
        print '   ', audio['url']
        print

    print 'Blog posts about ', top_hot.name
    for post in top_hot.blogs(rows=5):
        print '   ', post['name']
        print '   ', post['url']
        print

if __name__ == '__main__':
    main()
