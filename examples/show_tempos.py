# Shows the tempos for all of the songs in a director
# requires eyeD3, available from http://eyed3.nicfit.net/

import sys
import os
import eyeD3
import tempo


def show_tempo(mp3):
    "given an mp3, print out the artist, title and tempo of the song"
    tag = eyeD3.Tag()
    tag.link(mp3)
    my_tempo = tempo.get_tempo(tag.getArtist(), tag.getTitle())
    print 'File:  ', mp3
    print 'Artist:', tag.getArtist()
    print 'Title: ', tag.getTitle()
    print 'Tempo: ', my_tempo
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
