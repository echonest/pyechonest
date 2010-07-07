import urllib2
try:
    import json
except ImportError:
    import simplejson as json

from proxies import TrackProxy
import util

class Track(TrackProxy):
    """
    Represents an audio analysis from The Echo Nest.

    The track object will have the following properties:
    analysis_channels       an int
    analysis_sample_rate    a float
    analyzer_version        ex. '3.01a'
    artist                  ex. 'The Sea and Cake' or None
    bars                    a list of dicts
    beats                   a list of dicts
    bitrate                 an int
    duration                a float
    end_of_fade_in          a float
    id                      ex. 'TRTOBXJ1296BCDA33B'
    key                     an int
    key_confidence          a float
    loudness                a float
    md5                     ex. '17162ff555969cfed222e127837acd1a'
    meta                    a dict of analyzer data
    mode                    an int (0 or 1)
    mode_confidence         a float
    num_samples             an int
    release                 the album name, or None
    sample_md5              '4bf222fb6af22ba0226734bb978bac14'
    samplerate              an int
    sections                a list of dicts
    segments                a list of dicts
    start_of_fade_out       a float
    status                  ex. 'complete'
    tatums                  a list of dicts
    tempo                   a float
    tempo_confidence        a float
    title                   ex. 'Interiors' or None
    """

    def __repr__(self):
        try:
            return "<%s - %s>" % (self.type.encode('utf-8'), self.title.encode('utf-8'))
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
    else:
        track = result['track']
        identifier      = track.pop('id') 
        md5             = track.pop('md5', None) # tracks from song api calls will not have an md5
        audio_summary   = track.pop('audio_summary')
        json_url        = audio_summary['analysis_url']
        json_string     = urllib2.urlopen(json_url).read()
        analysis        = json.loads(json_string)
        nested_track    = analysis.pop('track')
        track.update(analysis)
        track.update(nested_track)
        track.update({'analysis_url': json_url})
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
    Convenience function for creating a track object from a file-like object
    """
    return _track_from_string(file_object.read(), filetype)

def track_from_filename(filename, filetype = None):
    """
    Convenience function for creating a track object from a file path
    if the filetype is none, we will get it from the extension
    """
    filetype = filetype or filename.split('.')[-1]
    return track_from_file(open(filename), filetype)

def track_from_url(url):
    """
    Convenience function for creating a track object from a public http url 
    """
    param_dict = dict(url = url)
    return _upload(param_dict) 
     
def track_from_id(identifier):
    """
    Convenience function for creating a track object from an id, like TRXXHTJ1294CD8F3B3
    """
    param_dict = dict(id = identifier)
    return _profile(param_dict)

def track_from_md5(md5):
    """
    Convenience function for creating a track object from an md5
    """
    param_dict = dict(md5 = md5)
    return _profile(param_dict)

def track_from_reanalyzing_id(identifier):
    """
    Convenience function for reanalzying an already uploaded track
    """
    param_dict = dict(id = identifier)
    return _analyze(param_dict)

def track_from_reanalyzing_md5(md5):
    """
    Convenience function for reanalzying an already uploaded track
    """
    param_dict = dict(md5 = md5)
    return _analyze(param_dict)
