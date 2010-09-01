#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2010-04-25.

The Playlist module loosely covers http://developer.echonest.com/docs/v4/playlist.html
Refer to the official api documentation if you are unsure about something.
"""

import util
from proxies import PlaylistProxy
from song import Song

class Playlist(PlaylistProxy):
    """
    A Dynamic Playlist object
    
    Create a dynamic playlist object like so:
        p = Playlist(type='artist-radio', artist=['ida maria', 'florence + the machine'])
    
    Attributes: (**attributes** are guaranteed to exist as soon as an artist object exists)
        **session_id**: Playlist Session ID
        **song**: The current song
    """
    
    def __init__(self, session_id=None, type='artist', artist_pick='song_hotttnesss-desc', variety=.5, artist_id=None, artist=None, \
                        song_id=None, description=None, max_tempo=None, min_tempo=None, max_duration=None, \
                        min_duration=None, max_loudness=None, min_loudness=None, max_danceability=None, min_danceability=None, \
                        max_complexity=None, min_complexity=None, artist_max_familiarity=None, artist_min_familiarity=None, \
                        artist_max_hotttnesss=None, artist_min_hotttnesss=None, song_max_hotttnesss=None, song_min_hotttnesss=None, \
                        min_longitude=None, max_longitude=None, min_latitude=None, max_latitude=None, \
                        mode=None, key=None, buckets=[], sort=None, limit=False, dmca=False, audio=False, chain_xspf=False):
        kwargs = {}
        if type:
            kwargs['type'] = type
        if artist_pick:
            kwargs['artist_pick'] = artist_pick
        if variety is not None:
            kwargs['variety'] = variety
        if artist:
            kwargs['artist'] = artist
        if artist_id:
            kwargs['artist_id'] = artist_id
        if song_id:
            kwargs['song_id'] = song_id
        if description:
            kwargs['description'] = description
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
        if dmca:
            kwargs['dmca'] = 'true'
        if chain_xspf:
            kwargs['chain_xspf'] = 'true'
        if audio:
            kwargs['audio'] = 'true'
        super(Playlist, self).__init__(session_id, **kwargs)
    
    def __repr__(self):
        return "<Dynamic Playlist - %s>" % self.session_id.encode('utf-8')
    
    # def __str__(self):
    #     return self.name.encode('utf-8')
    
    def get_next_song(self, **kwargs):
        response = self.get_attribute('dynamic', session_id=self.session_id, **kwargs)
        self.cache['songs'] = response['songs']
        # we need this to fix up all the dict keys to be strings, not unicode objects
        fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
        if len(self.cache['songs']):
            return Song(**fix(self.cache['songs'][0]))
        else:
            return None
    
    def get_current_song(self):
        # we need this to fix up all the dict keys to be strings, not unicode objects
        fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
        if not 'songs' in self.cache:
            self.get_next_song()
        if len(self.cache['songs']):
            return Song(**fix(self.cache['songs'][0]))
        else:
            return None

    song = property(get_current_song)

def static(type='artist', artist_pick='song_hotttnesss-desc', variety=.5, artist_id=None, artist=None, \
                    song_id=None, description=None, results=15, max_tempo=None, min_tempo=None, max_duration=None, \
                    min_duration=None, max_loudness=None, min_loudness=None, max_danceability=None, min_danceability=None, \
                    max_complexity=None, min_complexity=None, artist_max_familiarity=None, artist_min_familiarity=None, \
                    artist_max_hotttnesss=None, artist_min_hotttnesss=None, song_max_hotttnesss=None, song_min_hotttnesss=None, \
                    min_longitude=None, max_longitude=None, min_latitude=None, max_latitude=None, \
                    mode=None, key=None, buckets=[], sort=None, limit=False, audio=False):
    """get a static playlist"""
    kwargs = {}
    if type:
        kwargs['type'] = type
    if artist_pick:
        kwargs['artist_pick'] = artist_pick
    if variety is not None:
        kwargs['variety'] = variety
    if artist:
        kwargs['artist'] = artist
    if artist_id:
        kwargs['artist_id'] = artist_id
    if song_id:
        kwargs['song_id'] = song_id
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
    if audio:
        kwargs['audio'] = 'true' 
    
    result = util.callm("%s/%s" % ('playlist', 'static'), kwargs)
    # we need this to fix up all the dict keys to be strings, not unicode objects
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Song(**fix(s_dict)) for s_dict in result['response']['songs']]