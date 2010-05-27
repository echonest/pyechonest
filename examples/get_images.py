#!/usr/bin/env python
# encoding: utf-8
"""
get_images.py

Created by Jason Sundram on 2010-02-12.
"""
import os
import shutil
import sys
import urllib

# pyechonest imports. 
from pyechonest.artist import get_top_hottt_artists as hottt
from pyechonest.artist import search_artists

"""
Download images for the Echo Nest's top 1000 hottt artists, and 15 similar artists for each artist.
Files are named by Echo Nest Artist ID. All images that are large enough to look reasonable 
as part of a slideshow or screensaver are copied to a subfolder made in the current working 
directory called "big".

Optionally download images only for a given artist.
"""

usage = """
usage:
    python get_images.py [optional artist name]
    
    If you don't specify an artist name, images for the top 1000 hottt artists 
    and their similars will be downloaded.
    
    If you do specify an artist name, all images for that artist will be downloaded.
"""
# Maintain a record of artists that we already have images for, to avoid multiple downloads.
artists_with_images = set()

def has_images(artist_id):
    """Check to see if we've already downloaded an image for the given artist_id"""
    global artists_with_images
    if not artists_with_images:
        # See what images we've already got.
        # f: AR00B1I1187FB433EB_00.jpg -> AR00B1I1187FB433EB
        f = lambda x : x[:x.index('_')] 
        files = [i for i in os.listdir('.') if i.startswith('AR') and '_' in i]
        artists_with_images = set(map(f, files))
    return artist_id in artists_with_images
    
def copy_big(path='.', threshold=1000):
    """Copies the big images into a subfolder called 'big'. Creative, right?"""
    try:
        import Image
    except ImportError:
        sys.exit("copy_big requires PIL to work. Get it here: http://www.pythonware.com/products/pil/");
    big = os.path.join(path, 'big')
    if not os.path.exists(big):
        os.mkdir(big)
    l = os.listdir(path)
    for i in l:
        try:
            im = Image.open(i)
            if threshold < min(im.size):
                shutil.copyfile(i, os.path.join(big, i))
        except Exception, e:
            print "skipping %s: %s" % (i, e)

def safe(type, f):
    """ This catches any exception that might be thrown by f, and returns a new
        instance of type() instead. Use as follows r = safe(int, f)(args_for_f)
    """
    def wrapped(function, *args, **kwds):
        try:
            return function(*args, **kwds)
        except Exception, e:
            return type()
    return lambda *x,**k: wrapped(f,*x,**k)

def get_id(artist):
    """" 'music://id.echonest.com/~/AR/ARRX8P01187B99B26E' -> ARRX8P01187B99B26E"""
    i = artist.identifier
    return i[i.rfind('/')+1:]

def find_artist(artist_name):
    """Return a pyechonest artist for the given artist name."""
    matches = safe(list, search_artists)(artist_name)
    if matches:
        return matches[0]
    
    return None

def get_images(artist):
    """Retrieve all images for the given pyechonest artist."""
    enid = get_id(artist)
    if has_images(enid):
        print "skipping %s, already have images" % artist
        return
        
    images = safe(list, artist.images)() 
    for i, img in enumerate(images):
        try:
            print "getting image %d of %d for artist %s" % (i, len(images), artist.name)
            image = urllib.URLopener()
            url = img['url']
            # There's sometimes some crap after the file extension, most often #flat_doc,
            # e.g. http://userserve-ak.last.fm/serve/_/114442.jpg#flat_doc
            # I remove it here. Would be nice to do this more generally.
            ext = url[url.rfind('.'):].replace("#flat_doc", "")
            image.retrieve(url, "%s_%02d%s" % (enid, i, ext))
        except Exception, e:
            print e
            print "skipping %d" % i
    global artists_with_images
    artists_with_images.add(artist)

def download_hottt(count=1000):
    """Warning, downloading all these images takes a long time."""
    hottest = hottt(rows=count)
    for i, a in enumerate(hottest):
        print "Processing artist %d of %d" % (i, count)
        get_images(a)
        similars = safe(list, a.similar)()
        for s in similars:
            get_images(s)
    copy_big()

def main():
    if 2 <= len(sys.argv):
        name = ' '.join(sys.argv[1:])
        artist = find_artist(name)
        if artist:
            get_images(artist)
        else:
            print "Couldn't find artist %s" % name
    else:
        download_hottt()

if __name__ == '__main__':
    main()