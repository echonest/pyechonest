# Shows the tempos for all of the songs in a directory
# requires eyeD3, available from http://eyed3.nicfit.net/

import sys
import os

from pyechonest import track

AUDIO_EXTENSIONS = set(['mp3', 'm4a', 'wav', 'ogg', 'au', 'mp4'])

def _bar(val, ref=100, char='='):
    if val:
        num_chars = int(val * float(ref))
        return char * max(1, num_chars)
    else:
        return char

def _is_audio(f):
    _, ext = os.path.splitext(f)
    ext = ext[1:] # drop leading '.'
    return ext in AUDIO_EXTENSIONS
    
def _show_one(audiofile):
    "given an mp3, print out the artist, title and tempo of the song"
    print 'File:        ', audiofile
    pytrack = track.track_from_filename(audiofile)
    print 'Artist:      ', pytrack.artist if hasattr(pytrack, 'artist') else 'Unknown'
    print 'Title:       ', pytrack.title if hasattr(pytrack, 'title') else 'Unknown'
    print 'Tempo:       ', pytrack.tempo
    print 'Energy:       %1.3f %s' % (pytrack.energy, _bar(pytrack.energy))
    if not pytrack.valence:
        # Track hasn't had latest attributes computed. Force an upload.
        pytrack = track.track_from_filename(audiofile, force_upload=True)
    print 'Valence:      %1.3f %s' % (pytrack.valence, _bar(pytrack.valence)) 
    print 'Acousticness: %1.3f %s' % (pytrack.acousticness, _bar(pytrack.acousticness))
    print


def show_attrs(directory):
    "print out the tempo for each audio file in the given directory"
    for f in os.listdir(directory):
        if _is_audio(f):
            path = os.path.join(directory, f)
            _show_one(path)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'usage: python show_tempos.py path'
    else:
        show_attrs(sys.argv[1])
