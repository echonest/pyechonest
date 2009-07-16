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
import urllib
import socket

from pyechonest import artist, config

"""
Starting from an artist, build a playlist by wandering
around the artist neighborhood.
"""

usage = """
usage:
    python wander.py max artist name
"""
def wander(seed, max=10):
    """ generate a playlist by wandering a seed artist neighborhood """
    played = []
    while max:
        if seed.audio():
            audio = select_random_live_audio(seed.audio())
            if audio and audio['url'] not in played:
                if play(audio):
                    played.append(audio['url'])
                    max -= 1
        seed = random.choice(seed.similar())

def play(audio):
    if 'title' in audio and 'artist' in audio and 'url' in audio:
        print audio['title'],  "by", audio['artist'] 
        if  'link' in audio:
            print "   ", "From", audio['link'] 
        print "   ", audio['url'], "\n"
        return True
    return False

def select_random_live_audio(audio_list):
    random.shuffle(audio_list)
    for audio in audio_list:
        if is_live(audio['url']):
            return audio
    return None

def is_live(url):
    try:
        socket.setdefaulttimeout(5)
        f = urllib.urlopen(url)
        is_audio = f.info().gettype().find("audio") >= 0
        f.close()
        return is_audio
    except IOError:
        return False
        

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        max = int(sys.argv[1])
        args = sys.argv[2:]
        name = ' '.join(args)
        alist = artist.search_artists(name)
        if (len(alist) > 0):
            wander(alist[0], max)
        else :
            print "Can't find ", name
    else:
        print usage
        sys.exit(-1)
