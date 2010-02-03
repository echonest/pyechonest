#!/usr/bin/env python
# encoding: utf-8
"""
A Python interface to the The Echo Nest's web API.  See
http://developer.echonest.com/ for details.
"""
import hashlib
import os
import time

from decorators import memoized
import config
import util


class Track(object):
    def __init__(self, identifier):
        if os.path.isfile(identifier):
            # see if we already know about this track from the md5
            found = True
            analyzed = True
            md5 = calc_md5(identifier)
            if md5:
                try:
                   meta_data = get_metadata(md5)
                   if meta_data['status']=='UNAVAILABLE':
                       analyzed = False
                   self._md5 = meta_data['md5'] 
                   self._identifier = meta_data['id'] 
                except util.EchoNestAPIError:
                    found = False
            if not found:
                self._identifier = _upload(identifier)
                self._md5 = None
            elif not analyzed:
                self.params = {'md5': self._md5, 'analysis_version':config.ANALYSIS_VERSION}
                meta_data = self.analyze(wait=True)
        elif len(identifier)==18 and identifier.startswith('TR'):
            self._identifier = 'music://id.echonest.com/~/TR/' + identifier
            self._md5 = None
        elif len(identifier)==32:
            self._md5 = identifier
            self._identifier = None
        elif identifier.startswith('music://'):
            self._identifier = identifier
            self._md5 = None
        else:
            raise TypeError("Invalid identifier. Please supply filename, md5, or track ID.")
        self._name = None
        self.params = {'md5': self.md5, 'analysis_version':config.ANALYSIS_VERSION }

    def analyze(self, wait=False):
        """
        Re-analyze a previously uploaded track.
        """
        response = util.call('analyze', self.params, POST=True)
        metadata = self.metadata
        while wait:
            time.sleep(10)
            metadata = self.metadata
            if metadata.get('status')=='COMPLETE':
                wait = False
            else:
                wait = True
        return metadata
    
    # These are all lists of events (beats, etc)
    
    @property
    @memoized
    def bars(self):
        return parseToListOfEvents(util.call('get_bars', 
                                self.params).findall("analysis/bar"))

    @property
    @memoized
    def beats(self):
        return parseToListOfEvents(util.call('get_beats', 
                                self.params).findall("analysis/beat"))

    @property
    @memoized
    def tatums(self):
        return parseToListOfEvents(util.call('get_tatums', 
                                self.params).findall("analysis/tatum"))


    # These guys are all single float #s    
    
    @property
    @memoized
    def duration(self):
        return parseToFloat(util.call('get_duration', 
                                self.params).findall("analysis/duration"))
        
    @property
    @memoized
    def end_of_fade_in(self):
        return parseToFloat(util.call('get_end_of_fade_in', 
                                self.params).findall("analysis/end_of_fade_in"))
        
    @property
    @memoized
    def key(self):
        res = parseToFloat(util.call('get_key', 
                            self.params).findall("analysis/key"), 
                            with_confidence=True)
        res['value'] = int(res['value'])
        return res

    @property
    @memoized
    def loudness(self):
        return parseToFloat(util.call('get_loudness', 
                            self.params).findall("analysis/loudness"))

    @property
    @memoized
    def mode(self):
        res = parseToFloat(util.call('get_mode', 
                            self.params).findall("analysis/mode"), 
                            with_confidence=True)
        res['value'] = int(res['value'])
        return res

    @property
    @memoized
    def start_of_fade_out(self):
        return parseToFloat(util.call('get_start_of_fade_out', 
                            self.params).findall("analysis/start_of_fade_out"))

    @property
    @memoized
    def tempo(self):
        return parseToFloat(util.call('get_tempo', 
                            self.params).findall("analysis/tempo"), 
                            with_confidence=True)

    @property
    @memoized
    def time_signature(self):
        res = parseToFloat(util.call('get_time_signature', 
                            self.params).findall("analysis/time_signature"), 
                            with_confidence=True)
        res['value'] = int(res['value'])
        return res


    # And now the "special ones"
    
    @property
    @memoized
    def sections(self):
        tree = util.call('get_sections', self.params)
        output = []
        nodes = tree.findall('analysis/section')
        for n in nodes:
            start = float(n.attrib.get('start'))
            duration = float(n.attrib.get('duration'))
            output.append({"start":start,"duration":duration})
        return output

    @property
    #@memoized
    def metadata(self):
        if self._identifier is not None:
            params = {'id':self._identifier}
        else:
            params = {'md5':self._md5}
        params.update({'analysis_version':config.ANALYSIS_VERSION})
        tree = util.call('get_metadata', params)
        output = {}
        for n in tree.findall("analysis")[0].getchildren():
            output[n.tag] = n.text
        if output.has_key('status') and output['status']=='UNKNOWN':
            raise util.EchoNestAPIThingIDError(1, "Unknown track. Please upload.")
        return output

    def _metadata(self):
        if self._identifier is not None:
            params = {'id':self._identifier}
        else:
            params = {'md5':self._md5}
        params.update({'analysis_version':config.ANALYSIS_VERSION})
        tree = util.call('get_metadata', params)
        output = {}
        for n in tree.findall("analysis")[0].getchildren():
            output[n.tag] = n.text
        if output.has_key('status') and output['status']=='UNKNOWN':
            raise util.EchoNestAPIThingIDError(1, "Unknown track. Please upload.")
        return output

    @property
    @memoized
    def segments(self):
        tree = util.call('get_segments', self.params)
        output = []
        nodes = tree.findall('analysis/segment')
        for n in nodes:
            start = float(n.attrib.get('start'))
            duration = float(n.attrib.get('duration'))

            loudnessnodes = n.findall('loudness/dB')
            loudness_end = None
            for l in loudnessnodes:
                if 'type' in l.attrib:
                    time_loudness_max = float(l.attrib.get('time'))
                    loudness_max = float(l.text)
                else:
                    if float(l.attrib.get('time'))!=0:
                        loudness_end = float(l.text)
                    else:
                        loudness_begin = float(l.text)

            pitchnodes = n.findall('pitches/pitch')
            pitches=[]
            for p in pitchnodes:
                try:
                    pitches.append(float(p.text))
                except Exception:
                    pitches.append(0)

            timbrenodes = n.findall('timbre/coeff')
            timbre=[]
            for t in timbrenodes:
                try:
                    timbre.append(float(t.text))
                except Exception:
                    timbre.append(0)

            output.append({"start":start, "duration":duration, 
                            "pitches":pitches, "timbre":timbre,
                            "loudness_begin":loudness_begin,
                            "loudness_max":loudness_max,
                            "time_loudness_max":time_loudness_max,
                            "loudness_end":loudness_end})
        return output
        
    @property
    def identifier(self):
        """A unique identifier for a track.
        See http://developer.echonest.com/docs/datatypes/
        for more information"""
        if self._identifier is None:
            self._identifier = self.metadata['id']
        return self._identifier

    @property
    def name(self):
        if self._name is None:
            try:
                self._name = self.metadata['title']
            except KeyError:
                self._name = ""
        return self._name

    @property
    def md5(self):
        if self._md5 is None:
            self._md5 = self.metadata['md5']
        return self._md5

    def __repr__(self):
        return "<Track '%s'>" % self.name
    
    def __str__(self):
        return self.name


SEARCH_TRACKS_CACHE = {}
def search_tracks(name, start=0, rows=15, refresh=False):
    """Search for audio using a query on the track, album, or artist name."""
    global SEARCH_TRACKS_CACHE
    if config.CACHE and not refresh:
        try:
            return SEARCH_TRACKS_CACHE[(name, start, rows)]
        except KeyError:
            pass
    params = {'query': name, 'start': start, 'rows':rows}
    response = util.call('search_tracks', params).findall('results/doc')
    tracks = []
    for element in response:
        parsed = dict((e.tag, e.text) for e in element.getchildren())
        if element.attrib.has_key('id'):
            parsed.update({'id': element.attrib['id']})
        tracks.append(parsed)
    SEARCH_TRACKS_CACHE[(name, start, rows)] = tracks
    return SEARCH_TRACKS_CACHE[(name, start, rows)]


def get_top_hottt_tracks():
    response = util.call('get_top_hottt_tracks', {}).findall('results/doc')
    tracks = []
    for element in response:
        parsed = dict((e.tag, e.text) for e in element.getchildren())
        print parsed
        if element.attrib.has_key('id'):
            parsed.update({'id': element.attrib['id']})
        tracks.append(parsed)
    return tracks

def get_metadata(id_or_md5):
    is_id = False
    if len(id_or_md5)==18 and id_or_md5.startswith('TR'):
        is_id = True;
        id_or_md5 = 'music://id.echonest.com/~/TR/' + id_or_md5 
    elif id_or_md5.startswith('music://'):
        is_id = True;
    elif len(id_or_md5) == 32:
        is_id = False
    else:
        raise util.EchoNestAPIThingIDError(1, "bad ID or MD5")
    if is_id:
        params = {'id':id_or_md5}
    else:
        params = {'md5':id_or_md5}
    params.update({'analysis_version':config.ANALYSIS_VERSION})
    tree = util.call('get_metadata', params)
    output = {}
    for n in tree.findall("analysis")[0].getchildren():
        output[n.tag] = n.text
    if output.has_key('status') and output['status']=='UNKNOWN':
        raise util.EchoNestAPIError(1, "Unknown track. Please upload.")
    return output


def _analyze(md5_or_trackID, wait=True):
    """
    Re-analyze a previously uploaded track.
    """
    params = {'api_key':config.ECHO_NEST_API_KEY, 
                'version': 3, 
                'analysis_version':config.ANALYSIS_VERSION}
    if len(md5_or_trackID)==18 and md5_or_trackID.startswith('TR'):
        params['id'] = 'music://id.echonest.com/~/TR/' + md5_or_trackID
    elif md5_or_trackID.startswith('music://'):
        params['id'] = md5_or_trackID
    elif len(md5_or_trackID)==32:
        params['md5'] = md5_or_trackID
    response = util.call('analyze', params, POST=True)
    return response
    print response
    response = response.findall("track")
    print response
    if(len(response)>0):
        return Track(response[0].attrib.get("id"))
    else:
        return None


TRUTH = {True: 'Y', False: 'N'}

def upload(filename_or_url, wait=True):
    """
    Create a Track object based on the results of _upload().
    """
    result = _upload(filename_or_url, wait=wait)
    if result is not None:
        return Track(result)
    else:
        return None

def _upload(filename_or_url, wait=True):
    """
    Upload a file or give a URL to the EN analyze API.
    If you call this with wait=False it will return immediately.
    """
    if not filename_or_url.startswith("http://"):
        if os.path.isfile( filename_or_url ) : 
            # If file, upload using POST
            response = util.postChunked( host = config.API_HOST, 
                                     selector = config.API_SELECTOR + "upload",
                                     fields = {"api_key":config.ECHO_NEST_API_KEY, 
                                                "wait":TRUTH[wait], 'version': 3, 
                                                'analysis_version':config.ANALYSIS_VERSION}, 
                                     files = (( 'file', open(filename_or_url, 'rb')), )
                                     )
            response = util.parse_http_response(response).findall("track")
        else:
            raise Exception("File " + filename_or_url + " not found.")
    else :
        # Assume the filename is a URL. Call the upload method w/o a post.
        response = util.call('upload',{'url':filename_or_url, "wait":TRUTH[wait], 
                                        'analysis_version':config.ANALYSIS_VERSION}, 
                                        POST=True).findall("track")
    
    if len(response)>0:
        return response[0].attrib.get("id")
    else:
        return

def calc_md5(filename):
    try:
       return hashlib.md5(file(filename, 'rb').read()).hexdigest()
    except:
        return None

def parseToListOfEvents(evs):
    """
    parser for the list of events type calls
    """    
    events = []
    for x in evs:
        event = {}
        event["start"] = float(x.text)
        event["confidence"] = float(x.attrib.get("confidence"))
        events.append(event)
    return events
    
def parseToFloat(evs, with_confidence=False):
    """
    parser for the single float-type calls
    """
    ret = {}
    if(len(evs)):
        if(with_confidence):
            return {"value":float(evs[0].text), 
                    "confidence":float(evs[0].attrib.get("confidence"))}
        else:
            return float(evs[0].text)

