#!/usr/bin/env python
# encoding: utf-8
"""
show_artist.py

Created by Paul Lamere on 2009-06-29.
Copyright (c) 2009 The Echo Nest Corporation. All rights reserved.
"""

import sys
import os
from pyechonest import artist, config

"""
shows detailed info about an artist
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
        a = alist[0]

        print "Name:", a.name
        print "id:", a.identifier
        print "Familiarity:", a.familiarity()
        print "Hotttnesss:", a.hotttnesss()

        print "Similars:"
        for sim in a.similar():
            print "   ", sim.name

        print "Audio:"
        for audio in a.audio():
            if 'url' in audio:
                print "   ", audio['url']

        print "Blogs:"
        for blog in a.blogs():
            if 'name' in blog:
                print "   ", blog['name']

        print "News:"
        for news in a.news():
            if 'name' in news:
                print "   ", news['name']

        print "Reviews:"
        for review in a.reviews():
            if 'name' in review:
                print "   ", review['name']

        print "URLs:"
        for (name, url) in a.urls.items():
            print "   ", name, url[0:30];

        print "Videos:"
        for v in a.video():
            if 'site' in v and 'title' in v:
                print "   ", v['site'],  v['title']
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

