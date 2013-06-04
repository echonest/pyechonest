# Shows the tempos for all of the songs in a directory
# requires eyeD3, available from http://eyed3.nicfit.net/

import sys
import os
import tempo

from pyechonest import track

def show_tempo(mp3):
    "given an mp3, print out the artist, title and tempo of the song"
    pytrack = track.track_from_filename(mp3)
    print 'File:  ', mp3
    print 'Artist:', pytrack.artist if hasattr(pytrack, 'artist') else 'Unknown'
    print 'Title: ', pytrack.title if hasattr(pytrack, 'title') else 'Unknown'
    print 'Tempo: ', pytrack.tempo 
    print


def show_tempos(dir):
    "print out the tempo for each MP3 in the give directory"
    for f in os.listdir(dir):
        if f.lower().endswith(".mp3"):
            path = os.path.join(dir, f)
            show_tempo(path)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'usage: python show_tempos.py path'
    else:
        show_tempos(sys.argv[1])
