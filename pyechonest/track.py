import urllib2
try:
    import json
except ImportError:
    import simplejson as json

import hashlib
from proxies import TrackProxy
import util

class Track(TrackProxy):
    """
    Represents an audio analysis from The Echo Nest.

    All methods in this module return Track objects.

    Attributes:

        analysis_channels       int: the number of audio channels used during analysis
    
        analysis_sample_rate    float: the sample rate used during analysis
    
        analyzer_version        str: e.g. '3.01a'
    
        artist                  str or None: artist name
    
        bars                    list of dicts: timing of each measure
    
        beats                   list of dicts: timing of each beat
    
        bitrate                 int: the bitrate of the input mp3 (or other file)
        
        danceability            float: relative danceability (0 to 1)
    
        duration                float: length of track in seconds
        
        energy                  float: relative energy (0 to 1)
    
        end_of_fade_in          float: time in seconds track where fade-in ends
    
        id                      str: Echo Nest Track ID, e.g. 'TRTOBXJ1296BCDA33B'
    
        key                     int: between 0 (key of C) and 11 (key of B flat) inclusive
    
        key_confidence          float: confidence that key detection was accurate
    
        loudness                float: overall loudness in decibels (dB)
    
        md5                     str: 32-character checksum of the input mp3
    
        meta                    dict: other track metainfo
    
        mode                    int: 0 (major) or 1 (minor)
    
        mode_confidence         float: confidence that mode detection was accurate
    
        num_samples             int: total samples in the decoded track
    
        release                 str or None: the album name
    
        sample_md5              str: 32-character checksum of the decoded audio file
    
        samplerate              int: sample rate of input mp3
    
        sections                list of dicts: larger sections of song (chorus, bridge, solo, etc.)
    
        segments                list of dicts: timing, pitch, loudness and timbre for each segment
    
        start_of_fade_out       float: time in seconds where fade out begins
    
        status                  str: analysis status, e.g. 'complete', 'pending', 'error'
    
        tatums                  list of dicts: the smallest metrical unit (subdivision of a beat)
    
        tempo                   float: overall BPM (beats per minute)
    
        tempo_confidence        float: confidence that tempo detection was accurate
    
        title                   str or None: song title

    Each bar, beat, section, segment and tatum has a start time, a duration, and a confidence,
    in addition to whatever other data is given.
    
    Examples:
    
    >>> t = track.track_from_id('TRXXHTJ1294CD8F3B3')
    >>> t
    <track - Neverwas Restored (from Neverwas Soundtrack)>
    >>> t = track.track_from_md5('b8abf85746ab3416adabca63141d8c2d')
    >>> t
    <track - Neverwas Restored (from Neverwas Soundtrack)>
    >>> 
    """

    def __repr__(self):
        try:
            return "<%s - %s>" % (self._object_type.encode('utf-8'), self.title.encode('utf-8'))
        except AttributeError:
            # the title is None
            return "< Track >"
    
    def __str__(self):
        return self.title.encode('utf-8')

def _track_from_response(response):
    """
    This is the function that actually creates the track object
    """
    result = response['response']
    status = result['track']['status'].lower()
    if not status == 'complete':
        """
        pyechonest only supports wait = true for now, so this should not be pending
        """
        if status == 'error':
            raise Exception('there was an error analyzing the track')
        if status == 'pending':
            raise Exception('the track is still being analyzed')
        if status == 'forbidden':
            raise Exception('analysis of this track is forbidden')
        if status == 'unavailable':
            return track_from_reanalyzing_id(result['track']['id'])
    else:
        track = result['track']
        identifier      = track.pop('id') 
        md5             = track.pop('md5', None) # tracks from song api calls will not have an md5
        audio_summary   = track.pop('audio_summary')
        energy          = audio_summary.get('energy', 0)
        danceability    = audio_summary.get('danceability', 0)
        json_url        = audio_summary['analysis_url']
        json_string     = urllib2.urlopen(json_url).read()
        analysis        = json.loads(json_string)
        nested_track    = analysis.pop('track')
        track.update(analysis)
        track.update(nested_track)
        track.update({'analysis_url': json_url, 'energy': energy, 'danceability': danceability})
        return Track(identifier, md5, track)

def _upload(param_dict, data = None):
    """
    Calls upload either with a local audio file,
    or a url. Returns a track object.
    """
    param_dict['format'] = 'json'
    param_dict['wait'] = 'true'
    param_dict['bucket'] = 'audio_summary'
    result = util.callm('track/upload', param_dict, POST = True, socket_timeout = 300,  data = data) 
    return _track_from_response(result)

def _profile(param_dict):
    param_dict['format'] = 'json'
    param_dict['bucket'] = 'audio_summary'
    result = util.callm('track/profile', param_dict)
    return _track_from_response(result)

def _analyze(param_dict):
    param_dict['format'] = 'json'
    param_dict['bucket'] = 'audio_summary'
    param_dict['wait'] = 'true'
    result = util.callm('track/analyze', param_dict, POST = True, socket_timeout = 300)
    return _track_from_response(result)
    

""" Below are convenience functions for creating Track objects, you should use them """

def _track_from_string(audio_data, filetype):
    param_dict = {}
    param_dict['filetype'] = filetype 
    return _upload(param_dict, data = audio_data)

def track_from_file(file_object, filetype):
    """
    Create a track object from a file-like object.

    Args:
        file_object: a file-like Python object
        filetype: the file type (ex. mp3, ogg, wav)
    """
    try:
        hash = hashlib.md5(file_object.read()).hexdigest()
        return track_from_md5(hash)
    except util.EchoNestAPIError:
        file_object.seek(0)
        return _track_from_string(file_object.read(), filetype)

def track_from_filename(filename, filetype = None):
    """
    Create a track object from a filename.

    Args:
        filename: A string containing the path to the input file.
        filetype: A string indicating the filetype; Defaults to None (type determined by file extension).
    """
    filetype = filetype or filename.split('.')[-1]
    try:
        hash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
        return track_from_md5(hash)
    except util.EchoNestAPIError:
        return track_from_file(open(filename, 'rb'), filetype)

def track_from_url(url):
    """
    Create a track object from a public http URL.

    Args:
        url: A string giving the URL to read from. This must be on a public machine accessible by HTTP.
    """
    param_dict = dict(url = url)
    return _upload(param_dict) 
     
def track_from_id(identifier):
    """
    Create a track object from an Echo Nest track ID.

    Args:
        identifier: A string containing the ID of a track already analyzed (looks like "TRLMNOP12345678901").
    """
    param_dict = dict(id = identifier)
    return _profile(param_dict)

def track_from_md5(md5):
    """
    Create a track object from an md5 hash.

    Args:
        md5: A string 32 characters long giving the md5 checksum of a track already analyzed.
    """
    param_dict = dict(md5 = md5)
    return _profile(param_dict)

def track_from_reanalyzing_id(identifier):
    """
    Create a track object from an Echo Nest track ID, reanalyzing the track first.

    Args:
        identifier: A string containing the ID of a track already analyzed (looks like "TRLMNOP12345678901").
    """
    param_dict = dict(id = identifier)
    return _analyze(param_dict)

def track_from_reanalyzing_md5(md5):
    """
    Create a track object from an md5 hash, reanalyzing the track first.

    Args:
        md5: A string containing the md5 of a track already analyzed (looks like "TRLMNOP12345678901").
    """
    param_dict = dict(md5 = md5)
    return _analyze(param_dict)
