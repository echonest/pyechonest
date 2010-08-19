#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2010-04-25.

The Song module loosely covers http://developer.echonest.com/docs/v4/song.html
Refer to the official api documentation if you are unsure about something.
"""

import util
from proxies import SongProxy
from results import Result

try:
    import json
except ImportError:
    import simplejson as json
    
class Song(SongProxy):
    """
    A Song object
    
    Create a song object like so:
        s = song.Song('SOXZYYG127F3E1B7A2')
    
    Attributes: (**attributes** are guaranteed to exist as soon as an artist object exists)
        **id**: Echo Nest Song ID
        **title**: Song Title
        **artist_name**: Artist Name
        **artist_id**: Artist ID
        audio_summary: An Audio Summary Result object
        song_hotttnesss: A float representing a song's hotttnesss
        artist_hotttnesss: A float representing a song's parent artist's hotttnesss
        artist_familiarity: A float representing a song's parent artist's familiarity
        artist_location: A string specifying a song's parent artist's location
        tracks: A list of track result objects
    
    """
    def __init__(self, id, buckets = None, **kwargs):
        buckets = buckets or []
        super(Song, self).__init__(id, buckets, **kwargs)
    
    def __repr__(self):
        return "<%s - %s>" % (self.type.encode('utf-8'), self.title.encode('utf-8'))
    
    def __str__(self):
        return self.title.encode('utf-8')
    
        
    def get_audio_summary(self, cache=True):
        """Get an audio summary of a song containing mode, tempo, key, duration, time signature, loudness, and analysis_url.
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A dictionary containing mode, tempo, key, duration, time signature, loudness, and analysis_url keys.
        """
        if not (cache and ('audio_summary' in self.cache)):
            response = self.get_attribute('profile', bucket='audio_summary')
            self.cache['audio_summary'] = response['songs'][0]['audio_summary']
        return Result('audio_summary', self.cache['audio_summary'])
    
    audio_summary = property(get_audio_summary)
    
    def get_song_hotttnesss(self, cache=True):
        """Get our numerical description of how hottt a song currently is
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing hotttnesss.
        """
        if not (cache and ('song_hotttnesss' in self.cache)):
            response = self.get_attribute('profile', bucket='song_hotttnesss')
            self.cache['song_hotttnesss'] = response['songs'][0]['song_hotttnesss']
        return self.cache['song_hotttnesss']
    
    song_hotttnesss = property(get_song_hotttnesss)
    
    def get_artist_hotttnesss(self, cache=True):
        """Get our numerical description of how hottt a song's artist currently is
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing hotttnesss.
        """
        if not (cache and ('artist_hotttnesss' in self.cache)):
            response = self.get_attribute('profile', bucket='artist_hotttnesss')
            self.cache['artist_hotttnesss'] = response['songs'][0]['artist_hotttnesss']
        return self.cache['artist_hotttnesss']
    
    artist_hotttnesss = property(get_artist_hotttnesss)
    
    def get_artist_familiarity(self, cache=True):
        """Get our numerical estimation of how familiar a song's artist currently is to the world
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing familiarity.
        """
        if not (cache and ('artist_familiarity' in self.cache)):
            response = self.get_attribute('profile', bucket='artist_familiarity')
            self.cache['artist_familiarity'] = response['songs'][0]['artist_familiarity']
        return self.cache['artist_familiarity']
    
    artist_familiarity = property(get_artist_familiarity)
    
    def get_artist_location(self, cache=True):
        """Get the location of a song's artist.
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            An artist location object.
        """
        if not (cache and ('artist_location' in self.cache)):
            response = self.get_attribute('profile', bucket='artist_location')
            self.cache['artist_location'] = response['songs'][0]['artist_location']
        return Result('artist_location', self.cache['artist_location'])
    
    artist_location = property(get_artist_location)
    
    def get_tracks(self, catalog, limit=False):
        """Get the tracks for a song given a catalog.
        
        Args:
            catalog: a string representing the catalog whose track you want to retrieve.
        
        Returns:
            A list of Track IDs.
        """
        kwargs = {
            'method_name':'profile',
            'bucket':['tracks', 'id:%s' % catalog],
        }

        if limit:
            kwargs['limit'] = 'true'
        
        response = self.get_attribute(**kwargs)
        return response['songs'][0].get('tracks', [])

def identify(filename=None, query_obj=None, code=None, artist=None, title=None, release=None, duration=None, genre=None, buckets=None, alt=None, codegen_start=0, codegen_duration=30):
    kwargs = {}
    post = False
    has_data = False
    if filename:
        query_obj = util.codegen(filename, start=codegen_start, duration=codegen_duration)

    if not isinstance(query_obj, list):
        query_obj = [query_obj]

    if code:
        has_data = True
        kwargs['code'] = code
    if title:
        kwargs['title'] = title
    if release:
        kwargs['release'] = release
    if duration:
        kwargs['duration'] = duration
    if genre:
        kwargs['genre'] = genre
    if buckets:
        kwargs['bucket'] = buckets

    # TODO -- this is a temp debug param should be taken out for release
    if alt:
        if query_obj:
            query_obj[0]['alt'] = True

    if query_obj and any(query_obj):
        has_data = True
        kwargs['query'] = json.dumps(query_obj)
        post = True

    if has_data:
        result = util.callm("%s/%s" % ('song', 'identify'), kwargs, POST=post)
        print str(result)
        fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
        return [Song(**fix(s_dict)) for s_dict in result['response'].get('songs',[])]
    else:
        return None
    
    
    
def search(title=None, artist=None, artist_id=None, combined=None, description=None, results=None, max_tempo=None, \
                min_tempo=None, max_duration=None, min_duration=None, max_loudness=None, min_loudness=None, \
                artist_max_familiarity=None, artist_min_familiarity=None, artist_max_hotttnesss=None, \
                artist_min_hotttnesss=None, song_max_hotttnesss=None, song_min_hotttnesss=None, mode=None, \
                key=None, max_latitude=None, min_latitude=None, max_longitude=None, min_longitude=None, \
                sort=None, buckets = None, limit=False):
    """search for songs"""
    kwargs = {}
    if title:
        kwargs['title'] = title
    if artist:
        kwargs['artist'] = artist
    if artist_id:
        kwargs['artist_id'] = artist_id
    if combined:
        kwargs['combined'] = combined
    if description:
        kwargs['description'] = description
    if results is not None:
        kwargs['results'] = results
    if max_tempo is not None:
        kwargs['max_tempo'] = max_tempo
    if min_tempo is not None:
        kwargs['min_tempo'] = min_tempo
    if max_duration is not None:
        kwargs['max_duration'] = max_duration
    if min_duration is not None:
        kwargs['min_duration'] = min_duration
    if max_loudness is not None:
        kwargs['max_loudness'] = max_loudness
    if min_loudness is not None:
        kwargs['min_loudness'] = min_loudness
    if artist_max_familiarity is not None:
        kwargs['artist_max_familiarity'] = artist_max_familiarity
    if artist_min_familiarity is not None:
        kwargs['artist_min_familiarity'] = artist_min_familiarity
    if artist_max_hotttnesss is not None:
        kwargs['artist_max_hotttnesss'] = artist_max_hotttnesss
    if artist_min_hotttnesss is not None:
        kwargs['artist_min_hotttnesss'] = artist_min_hotttnesss
    if song_max_hotttnesss is not None:
        kwargs['song_max_hotttnesss'] = song_max_hotttnesss
    if song_min_hotttnesss is not None:
        kwargs['song_min_hotttnesss'] = song_min_hotttnesss
    if mode is not None:
        kwargs['mode'] = mode
    if key is not None:
        kwargs['key'] = key
    if max_latitude is not None:
        kwargs['max_latitude'] = max_latitude
    if min_latitude is not None:
        kwargs['min_latitude'] = min_latitude
    if max_longitude is not None:
        kwargs['max_longitude'] = max_longitude
    if min_longitude is not None:
        kwargs['min_longitude'] = min_longitude
    if sort:
        kwargs['sort'] = sort
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    
    result = util.callm("%s/%s" % ('song', 'search'), kwargs)
    # we need this to fix up all the dict keys to be strings, not unicode objects
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Song(**fix(s_dict)) for s_dict in result['response']['songs']]

def profile(ids, buckets = None, limit=False):
    """get the profiles for multiple songs at once"""
    buckets = buckets or []
    if not isinstance(ids, list):
        ids = [ids]
    kwargs = {}
    kwargs['id'] = ids
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    
    result = util.callm("%s/%s" % ('song', 'profile'), kwargs)
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Song(**fix(s_dict)) for s_dict in result['response']['songs']]

