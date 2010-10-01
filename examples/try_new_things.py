#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2010-09-01

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
"""

# ========================
# = try_new_things.py =
# ========================
#
# enter a few of your favorite artists and create a playlist of new music that 
# you might like. 
#

import sys, os, logging
import xml.sax.saxutils as saxutils
from optparse import OptionParser
from pyechonest import artist, playlist

# set your api key here if it's not set in the environment
# config.ECHO_NEST_API_KEY = "XXXXXXXXXXXXXXXXX"
logger = logging.getLogger(__name__)

class XmlWriter(object):
    """ code from: http://users.musicbrainz.org/~matt/xspf/m3u2xspf
        Copyright (c) 2006, Matthias Friedrich <matt@mafr.de>
    """
    def __init__(self, outStream, indentAmount='  '):
        self._out = outStream
        self._indentAmount = indentAmount
        self._stack = [ ]
    
    def prolog(self, encoding='UTF-8', version='1.0'):
        pi = '<?xml version="%s" encoding="%s"?>' % (version, encoding)
        self._out.write(pi + '\n')
    
    def start(self, name, attrs={ }):
        indent = self._getIndention()
        self._stack.append(name)
        self._out.write(indent + self._makeTag(name, attrs) + '\n')
    
    def end(self):
        name = self._stack.pop()
        indent = self._getIndention()
        self._out.write('%s</%s>\n' % (indent, name))
    
    def elem(self, name, value, attrs={ }):
        # delete attributes with an unset value
        for (k, v) in attrs.items():
            if v is None or v == '':
                del attrs[k]
        
        if value is None or value == '':
            if len(attrs) == 0:
                return
            self._out.write(self._getIndention())
            self._out.write(self._makeTag(name, attrs, True) + '\n')
        else:
            escValue = saxutils.escape(value or '')
            self._out.write(self._getIndention())
            self._out.write(self._makeTag(name, attrs))
            self._out.write(escValue)
            self._out.write('</%s>\n' % name)
    
    def _getIndention(self):
        return self._indentAmount * len(self._stack)
    
    def _makeTag(self, name, attrs={ }, close=False):
        ret = '<' + name
    
        for (k, v) in attrs.iteritems():
            if v is not None:
                v = saxutils.quoteattr(str(v))
                ret += ' %s=%s' % (k, v)
        
        if close:
            return ret + '/>'
        else:
            return ret + '>'
            

            
def write_xspf(f, tuples):
    """send me a list of (artist,title,mp3_url)"""
    xml = XmlWriter(f, indentAmount='  ')
    xml.prolog()
    xml.start('playlist', { 'xmlns': 'http://xspf.org/ns/0/', 'version': '1' })
    xml.start('trackList')
    for tupe in tuples:
        xml.start('track')
        xml.elem('creator',tupe[0])
        xml.elem('title',tupe[1])
        xml.elem('location', tupe[2])
        xml.end()
    xml.end()
    xml.end()
    f.close()


def lookup_seeds(seed_artist_names):
    seed_ids = []
    for artist_name in seed_artist_names:
        try:
            seed_ids.append("-%s" % (artist.Artist(artist_name).id,))
        except Exception:
            logger.info('artist "%s" not found.' % (artist_name,))
            # we could try to do full artist search here
            # and let them choose the right artist
    logger.info('seed_ids: %s' % (seed_ids,))
    return seed_ids


def find_playlist(seed_artist_ids, playable=False):
    if playable:
        logger.info("finding playlist with audio...")
        p = playlist.static(type='artist-radio', artist_id=seed_artist_ids, variety=1, buckets=['id:7digital', 'tracks'], limit=True)
    else:
        logger.info("finding playlist without audio...")
        p = playlist.static(type='artist-radio', artist_id=seed_artist_ids, variety=1)
    return p



if __name__ == "__main__":
    usage = 'usage: %prog [options] "artist 1" "artist 2" ... "artist N"\n\n' \
    'example:\n' \
    '\t ./%prog "arcade fire" "feist" "broken social scene" -x -f arcade_feist_scene.xspf\n' \
    '\t ./%prog "justice" "four tet" "bitshifter" -v\n'
    
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="say what you're doing")
    parser.add_option("-a", "--audio",
                      action="store_true", dest="audio", default=False,
                      help="fetch sample audio for songs")
    parser.add_option("-x", "--xspf",
                      action="store_true", dest="xspf", default=False,
                      help="output an xspf format playlist")
    parser.add_option("-f", "--filename",
                      metavar="FILE", help="write output to FILE")

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("you must provide at least 1 seed artist!")

    # handle verbose logging
    log_level = logging.ERROR
    if options.verbose:
        log_level = logging.INFO
    logging.basicConfig(level=log_level)
    logger.setLevel(log_level)
    
    # make sure output file doesn't already exist
    if options.filename and os.path.exists(options.filename):
        logger.error("The file path: %s already exists." % (options.filename,))
        sys.exit(1)

    # resolve seed artists
    seed_ids = lookup_seeds(args)

    # find playlist
    raw_plist = find_playlist(seed_ids, playable=(options.audio or options.xspf))
    
    tuple_plist = []
    for s in raw_plist:
        name = s.artist_name
        title = s.title
        url = ""
        if options.audio:
            url = s.get_tracks('7digital', [{}])[0].get('preview_url')
        tuple_plist.append((name,title,url))

    # write to stdout or file specified
    fout = open(options.filename, 'w') if options.filename else sys.stdout
    if options.xspf:
        write_xspf(fout, tuple_plist)
    else:
        for tupe in tuple_plist:
            fout.write("%s - %s \t %s\n" % tupe)
    logger.info("all done!")
    sys.exit(0)