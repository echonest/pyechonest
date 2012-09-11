import urllib2
try:
    import json
except ImportError:
    import simplejson as json

import hashlib
from proxies import TrackProxy
import util
import time

# Seconds to wait for asynchronous track/upload or track/analyze jobs to complete.
# Previously the socket timeouts on the synchronous calls were 300 secs.
DEFAULT_ASYNC_TIMEOUT = 300

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
    
        speechiness             float: relative speechiness (0 to 1)
    
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

def _wait_for_pending_track(trid, timeout):
    # timeout is ignored for now
    status = 'pending'
    while status == 'pending':
        time.sleep(1)
        param_dict = {'id': trid} # dict(id = identifier)
        param_dict['format'] = 'json'
        param_dict['bucket'] = 'audio_summary'
        result = util.callm('track/profile', param_dict)
        status = result['response']['track']['status'].lower()
        # TODO: timeout if necessary
    return result

def _track_from_response(result, timeout=DEFAULT_ASYNC_TIMEOUT):
    """
    This is the function that actually creates the track object
    """
    response = result['response']
    status = response['track']['status'].lower()

    if status == 'pending':
        # Need to wait for async upload or analyze call to finish.
        result = _wait_for_pending_track(response['track']['id'], timeout)
        response = result['response']
        status = response['track']['status'].lower()
            
    if not status == 'complete':
        if status == 'pending':
            # Operation didn't complete by timeout above.
            raise Exception('the operation didn\'t complete before the timeout (%d secs)' % timeout)
        elif status == 'error':
            raise Exception('there was an error analyzing the track')
        elif status == 'forbidden':
            raise Exception('analysis of this track is forbidden')
        if status == 'unavailable':
            return track_from_reanalyzing_id(result['track']['id'])
    else:
        track = response['track']
        identifier      = track.pop('id') 
        md5             = track.pop('md5', None) # tracks from song api calls will not have an md5
        audio_summary   = track.pop('audio_summary')
        energy          = audio_summary.get('energy', 0)
        danceability    = audio_summary.get('danceability', 0)
        speechiness     = audio_summary.get('speechiness', 0)
        json_url        = audio_summary.get('analysis_url')
        if json_url:
            try:
                json_string = urllib2.urlopen(json_url).read()
                analysis = json.loads(json_string)
            except: #pylint: disable=W0702
                analysis = {}
        else:
            analysis = {}
        nested_track    = analysis.pop('track', {})
        track.update(analysis)
        track.update(nested_track)
    track.update({'analysis_url': json_url, 'energy': energy,
                  'danceability': danceability,
                  'speechiness': speechiness})
    return Track(identifier, md5, track)

def _upload(param_dict, timeout, data = None):
    """
    Calls upload either with a local audio file,
    or a url. Returns a track object.
    """
    param_dict['format'] = 'json'
    param_dict['wait'] = 'true'
    param_dict['bucket'] = 'audio_summary'
    result = util.callm('track/upload', param_dict, POST = True, socket_timeout = 300,  data = data) 
    return _track_from_response(result, timeout)

def _profile(param_dict):
    param_dict['format'] = 'json'
    param_dict['bucket'] = 'audio_summary'
    result = util.callm('track/profile', param_dict)
    return _track_from_response(result)

def _analyze(param_dict, timeout):
    param_dict['format'] = 'json'
    param_dict['bucket'] = 'audio_summary'
    param_dict['wait'] = 'true'
    result = util.callm('track/analyze', param_dict, POST = True, socket_timeout = 300)
    return _track_from_response(result, timeout)
    

""" Below are convenience functions for creating Track objects, you should use them """

def _track_from_data(audio_data, filetype, timeout):
    param_dict = {}
    param_dict['filetype'] = filetype 
    return _upload(param_dict, timeout, data = audio_data)

def track_from_file(file_object, filetype, timeout=DEFAULT_ASYNC_TIMEOUT):
    """
    Create a track object from a file-like object.

    Args:
        file_object: a file-like Python object
        filetype: the file type (ex. mp3, ogg, wav)
    
    Example:
        >>> f = open("Miaow-01-Tempered-song.mp3")
        >>> t = track.track_from_file(f, 'mp3')
        >>> t
        < Track >
        >>>
    """
    try:
        hash = hashlib.md5(file_object.read()).hexdigest()
        return track_from_md5(hash)
    except util.EchoNestAPIError:
        file_object.seek(0)
        return _track_from_data(file_object.read(), filetype, timeout)

def track_from_filename(filename, filetype = None, timeout=DEFAULT_ASYNC_TIMEOUT):
    """
    Create a track object from a filename.

    Args:
        filename: A string containing the path to the input file.
        filetype: A string indicating the filetype; Defaults to None (type determined by file extension).
    
    Example:
        >>> t = track.track_from_filename("Miaow-01-Tempered-song.mp3")
        >>> t
        < Track >
        >>>
    """
    filetype = filetype or filename.split('.')[-1]
    try:
        md5 = hashlib.md5(open(filename, 'rb').read()).hexdigest()
        return track_from_md5(md5)
    except util.EchoNestAPIError:
        return _track_from_data(open(filename, 'rb').read(), filetype, timeout)

def track_from_url(url, timeout=DEFAULT_ASYNC_TIMEOUT):
    """
    Create a track object from a public http URL.

    Args:
        url: A string giving the URL to read from. This must be on a public machine accessible by HTTP.
    
    Example:
        >>> t = track.track_from_url("http://www.miaowmusic.com/mp3/Miaow-01-Tempered-song.mp3")
        >>> t
        < Track >
        >>>
        
    """
    param_dict = dict(url = url)
    return _upload(param_dict, timeout) 
     
def track_from_id(identifier):
    """
    Create a track object from an Echo Nest track ID.

    Args:
        identifier: A string containing the ID of a previously analyzed track.
    
    Example:
        >>> t = track.track_from_id("TRWFIDS128F92CC4CA")
        >>> t
        <track - Let The Spirit>
        >>>
    """
    param_dict = dict(id = identifier)
    return _profile(param_dict)

def track_from_md5(md5):
    """
    Create a track object from an md5 hash.

    Args:
        md5: A string 32 characters long giving the md5 checksum of a track already analyzed.
    
    Example:
        >>> t = track.track_from_md5('b8abf85746ab3416adabca63141d8c2d')
        >>> t
        <track - Neverwas Restored (from Neverwas Soundtrack)>
        >>>
    """
    param_dict = dict(md5 = md5)
    return _profile(param_dict)

def track_from_reanalyzing_id(identifier, timeout=DEFAULT_ASYNC_TIMEOUT):
    """
    Create a track object from an Echo Nest track ID, reanalyzing the track first.

    Args:
        identifier (str): A string containing the ID of a previously analyzed track
    
    Example:
        >>> t = track.track_from_reanalyzing_id('TRXXHTJ1294CD8F3B3')
        >>> t
        <track - Neverwas Restored>
        >>>
    """
    param_dict = dict(id = identifier)
    return _analyze(param_dict, timeout)

def track_from_reanalyzing_md5(md5, timeout=DEFAULT_ASYNC_TIMEOUT):
    """
    Create a track object from an md5 hash, reanalyzing the track first.

    Args:
        md5 (str): A string containing the md5 of a previously analyzed track

    Example:
        >>> t = track.track_from_reanalyzing_md5('b8abf85746ab3416adabca63141d8c2d')
        >>> t
        <track - Neverwas Restored>
        >>>
    """
    param_dict = dict(md5 = md5)
    return _analyze(param_dict, timeout)
