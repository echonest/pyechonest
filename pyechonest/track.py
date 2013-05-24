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
DEFAULT_ASYNC_TIMEOUT = 60

class Track(TrackProxy):
    """
    Represents an audio file and its analysis from The Echo Nest.
    All public methods in this module return Track objects.

    Depending on the information available, a Track may have some or all of the
    following attributes:

        acousticness            float: confidence the track is "acoustic" (0.0 to 1.0)
        analysis_url            URL to retrieve the complete audio analysis (time expiring)
        analyzer_version        str: e.g. '3.01a'
        artist                  str or None: artist name
        artist_id               Echo Nest ID of artist, if known
        danceability            float: relative danceability (0.0 to 1.0)
        duration                float: length of track in seconds
        energy                  float: relative energy (0.0 to 1.0)
        id                      str: Echo Nest Track ID, e.g. 'TRTOBXJ1296BCDA33B'
        key                     int: between 0 (key of C) and 11 (key of B flat) inclusive
        liveness                float: confidence the track is "live" (0.0 to 1.0)
        loudness                float: overall loudness in decibels (dB)
        md5                     str: 32-character checksum of the original audio file, if available
        mode                    int: 0 (major) or 1 (minor)
        song_id                 The Echo Nest song ID for the track, if known
        speechiness             float: likelihood the track contains speech (0.0 to 1.0)
        status                  str: analysis status, e.g. 'complete'
        tempo                   float: overall BPM (beats per minute)
        time_signature          beats per measure (e.g. 3, 4, 5, 7)
        title                   str or None: song title
        valence                 float: a range from negative to positive emotional content (0.0 to 1.0)

    The following attributes are available only after calling Track.get_analysis():
    
        analysis_channels       int: the number of audio channels used during analysis
        analysis_sample_rate    int: the sample rate used during analysis
        bars                    list of dicts: timing of each measure
        beats                   list of dicts: timing of each beat
        codestring              ENMFP code string
        code_version            version of ENMFP code generator
        decoder                 audio decoder used by the analysis (e.g. ffmpeg)
        echoprintstring         fingerprint string using Echoprint (http://echoprint.me)
        echoprint_version       version of Echoprint code generator
        end_of_fade_in          float: time in seconds track where fade-in ends
        key_confidence          float: confidence that key detection was accurate
        meta                    dict: other track metainfo (bitrate, album, genre, etc.)
        mode_confidence         float: confidence that mode detection was accurate
        num_samples             int: total samples in the decoded track
        offset_seconds          unused, always 0
        sample_md5              str: 32-character checksum of the decoded audio file
        samplerate              the audio sample rate detected in the file
        sections                list of dicts: larger sections of song (chorus, bridge, solo, etc.)
        segments                list of dicts: timing, pitch, loudness and timbre for each segment
        start_of_fade_out       float: time in seconds where fade out begins
        synchstring             string providing synchronization points throughout the track
        synch_version           version of the synch string algorithm
        tatums                  list of dicts: the smallest metrical unit (subdivision of a beat)
        tempo_confidence        float: confidence that tempo detection was accurate
        time_signature_confidence float: confidence that time_signature detection was accurate
    
    Each bar, beat, section, segment and tatum has a start time, a duration, and a confidence,
    in addition to whatever other data is given.

    Examples:

    >>> t = track.track_from_id('TRJSEBQ1390EC0B548')
    >>> t
    <track - Dark Therapy>

    >>> t = track.track_from_md5('96fa0180d225f14e9f8cbfffbf5eb81d')
    >>> t
    <track - Spoonful - Live At Winterland>
    >>>

    >>> t = track.track_from_filename('Piano Man.mp3')
    >>> t.meta
    AttributeError: 'Track' object has no attribute 'meta'
    >>> t.get_analysis()
    >>> t.meta
    {u'album': u'Piano Man',
     u'analysis_time': 8.9029500000000006,
     u'analyzer_version': u'3.1.3',
     u'artist': u'Billy Joel',
     u'bitrate': 160,
     u'detailed_status': u'OK',
     u'filename': u'/tmp/tmphrBQL9/fd2b524958548e7ecbaf758fb675fab1.mp3',
     u'genre': u'Soft Rock',
     u'sample_rate': 44100,
     u'seconds': 339,
     u'status_code': 0,
     u'timestamp': 1369400122,
     u'title': u'Piano Man'}
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
        
    def get_analysis(self):
        """ Retrieve the detailed analysis for the track, if available. 
            Raises Exception if unable to create the detailed analysis. """
        if self.analysis_url:
            try:
                # Try the existing analysis_url first. This expires shortly
                # after creation.
                try:
                    json_string = urllib2.urlopen(self.analysis_url).read()
                except urllib2.HTTPError:
                    # Probably the analysis_url link has expired. Refresh it.
                    param_dict = dict(id = self.id)
                    new_track = _profile(param_dict, DEFAULT_ASYNC_TIMEOUT)
                    if new_track and new_track.analysis_url:
                        self.analysis_url = new_track.analysis_url
                        json_string = urllib2.urlopen(self.analysis_url).read()
                    else:
                        raise Exception("Failed to create track analysis.")

                analysis = json.loads(json_string)
                analysis_track = analysis.pop('track', {})
                self.__dict__.update(analysis)
                self.__dict__.update(analysis_track)
            except Exception: #pylint: disable=W0702
                # No detailed analysis found.
                raise Exception("Failed to create track analysis.")
        else:
            raise Exception("Failed to create track analysis.")


def _wait_for_pending_track(trid, timeout):
    status = 'pending'
    param_dict = {'id': trid}
    param_dict['format'] = 'json'
    param_dict['bucket'] = 'audio_summary'
    start_time = time.time()
    end_time = start_time + timeout
    # counter for seconds to wait before checking track profile again.
    timeout_counter = 3
    while status == 'pending' and time.time() < end_time:
        time.sleep(timeout_counter)
        result = util.callm('track/profile', param_dict)
        status = result['response']['track']['status'].lower()
        # Slowly increment to wait longer each time.
        timeout_counter += timeout_counter / 2
    return result

def _track_from_response(result, timeout):
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
        track_id = response['track']['id']
        if status == 'pending':
            raise Exception('%s: the operation didn\'t complete before the timeout (%d secs)' %
                            (track_id, timeout))
        else:
            raise Exception('%s: there was an error analyzing the track, status: %s' % (track_id, status))
    else:
        # track_properties starts as the response dictionary.
        track_properties = response['track']
        # 'id' and 'md5' are separated to construct the Track object.
        identifier = track_properties.pop('id')
        md5        = track_properties.pop('md5', None) # tracks from song api calls will not have an md5
        # Pop off the audio_summary dict and make those keys attributes
        # of the Track. This includes things like tempo, energy, and loudness.
        track_properties.update(track_properties.pop('audio_summary'))
        return Track(identifier, md5, track_properties)

def _upload(param_dict, timeout, data):
    """
    Calls upload either with a local audio file,
    or a url. Returns a track object.
    """
    param_dict['format'] = 'json'
    param_dict['wait'] = 'true'
    param_dict['bucket'] = 'audio_summary'
    result = util.callm('track/upload', param_dict, POST = True, socket_timeout = 300,  data = data)
    return _track_from_response(result, timeout)

def _profile(param_dict, timeout):
    param_dict['format'] = 'json'
    param_dict['bucket'] = 'audio_summary'
    result = util.callm('track/profile', param_dict)
    return _track_from_response(result, timeout)


""" Below are convenience functions for creating Track objects, you should use them """

def _track_from_data(audio_data, filetype, timeout):
    param_dict = {}
    param_dict['filetype'] = filetype
    return _upload(param_dict, timeout, audio_data)

def track_from_file(file_object, filetype, timeout=DEFAULT_ASYNC_TIMEOUT, force_upload=False):
    """
    Create a track object from a file-like object.

    NOTE: Does not create the detailed analysis for the Track. Call
    Track.get_analysis() for that.

    Args:
        file_object: a file-like Python object
        filetype: the file type. Supported types include mp3, ogg, wav, m4a, mp4, au
        force_upload: skip the MD5 shortcut path, force an upload+analysis
    Example:
        >>> f = open("Miaow-01-Tempered-song.mp3")
        >>> t = track.track_from_file(f, 'mp3')
        >>> t
        < Track >
        >>>
    """
    if not force_upload:
        try:
            # Check if this file has already been uploaded.
            # This is much faster than uploading.
            md5 = hashlib.md5(file_object.read()).hexdigest()
            return track_from_md5(md5)
        except util.EchoNestAPIError:
            # Fall through to do a fresh upload.
            pass

    file_object.seek(0)
    return _track_from_data(file_object.read(), filetype, timeout)

def track_from_filename(filename, filetype = None, timeout=DEFAULT_ASYNC_TIMEOUT, force_upload=False):
    """
    Create a track object from a filename.

    NOTE: Does not create the detailed analysis for the Track. Call
    Track.get_analysis() for that.

    Args:
        filename: A string containing the path to the input file.
        filetype: A string indicating the filetype; Defaults to None (type determined by file extension).
        force_upload: skip the MD5 shortcut path, force an upload+analysis

    Example:
        >>> t = track.track_from_filename("Miaow-01-Tempered-song.mp3")
        >>> t
        < Track >
        >>>
    """
    filetype = filetype or filename.split('.')[-1]
    file_object = open(filename, 'rb')
    result = track_from_file(file_object, filetype, timeout, force_upload)
    file_object.close()
    return result

def track_from_url(url, timeout=DEFAULT_ASYNC_TIMEOUT):
    """
    Create a track object from a public http URL.

    NOTE: Does not create the detailed analysis for the Track. Call
    Track.get_analysis() for that.

    Args:
        url: A string giving the URL to read from. This must be on a public machine accessible by HTTP.

    Example:
        >>> t = track.track_from_url("http://www.miaowmusic.com/mp3/Miaow-01-Tempered-song.mp3")
        >>> t
        < Track >
        >>>

    """
    param_dict = dict(url = url)
    return _upload(param_dict, timeout, data=None)

def track_from_id(identifier, timeout=DEFAULT_ASYNC_TIMEOUT):
    """
    Create a track object from an Echo Nest track ID.

    NOTE: Does not create the detailed analysis for the Track. Call
    Track.get_analysis() for that.

    Args:
        identifier: A string containing the ID of a previously analyzed track.

    Example:
        >>> t = track.track_from_id("TRWFIDS128F92CC4CA")
        >>> t
        <track - Let The Spirit>
        >>>
    """
    param_dict = dict(id = identifier)
    return _profile(param_dict, timeout)

def track_from_md5(md5, timeout=DEFAULT_ASYNC_TIMEOUT):
    """
    Create a track object from an md5 hash.

    NOTE: Does not create the detailed analysis for the Track. Call
    Track.get_analysis() for that.

    Args:
        md5: A string 32 characters long giving the md5 checksum of a track already analyzed.

    Example:
        >>> t = track.track_from_md5('b8abf85746ab3416adabca63141d8c2d')
        >>> t
        <track - Neverwas Restored (from Neverwas Soundtrack)>
        >>>
    """
    param_dict = dict(md5 = md5)
    return _profile(param_dict, timeout)
