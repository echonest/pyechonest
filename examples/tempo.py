import sys
from pyechonest import song

def get_tempo(artist, title):
    "gets the tempo for a song"
    results = song.search(artist=artist, title=title, results=1, buckets=['audio_summary'])
    if len(results) > 0:
        return results[0].audio_summary.tempo
    else:
        return None


if __name__ == '__main__':
    if len(sys.argv) <> 3:
        print "Usage: python tempo.py 'artist name' 'song title'"
    else:
        tempo = get_tempo(sys.argv[1], sys.argv[2])
        if tempo:
            print 'Tempo for', sys.argv[1], sys.argv[2], 'is', tempo
        else:
            print "Can't find Tempo for artist:", sys.argv[1], 'song:', sys.argv[2]
        

