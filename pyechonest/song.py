#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2010-04-25.

The Song module loosely covers http://developer.echonest.com/docs/v4/song.html
Refer to the official api documentation if you are unsure about something.
"""
import os
import util
from proxies import SongProxy

try:
    import json
except ImportError:
    import simplejson as json
    
class Song(SongProxy):
    """
    A Song object
    
    Attributes: 
        id (str): Echo Nest Song ID
        
        title (str): Song Title
        
        artist_name (str): Artist Name
        
        artist_id (str): Artist ID
        
        audio_summary (dict): An Audio Summary dict
        
        song_hotttnesss (float): A float representing a song's hotttnesss
        
        artist_hotttnesss (float): A float representing a song's parent artist's hotttnesss
        
        artist_familiarity (float): A float representing a song's parent artist's familiarity
        
        artist_location (dict): A dictionary of strings specifying a song's parent artist's location, lattitude and longitude
        
    Create a song object like so:

    >>> s = song.Song('SOPEXHZ12873FD2AC7')
    
    """
    def __init__(self, id, buckets=None, **kwargs):
        """
        Song class
        
        Args:
            id (str): a song ID 

        Kwargs:
            buckets (list): A list of strings specifying which buckets to retrieve

        Returns:
            A Song object

        Example:

        >>> s = song.Song('SOPEXHZ12873FD2AC7', buckets=['song_hotttnesss', 'artist_hotttnesss'])
        >>> s.song_hotttnesss
        0.58602500000000002
        >>> s.artist_hotttnesss
        0.80329715999999995
        >>> 

        """
        buckets = buckets or []
        super(Song, self).__init__(id, buckets, **kwargs)
    
    def __repr__(self):
        return "<%s - %s>" % (self._object_type.encode('utf-8'), self.title.encode('utf-8'))
    
    def __str__(self):
        return self.title.encode('utf-8')
    
        
    def get_audio_summary(self, cache=True):
        """Get an audio summary of a song containing mode, tempo, key, duration, time signature, loudness, danceability, energy, and analysis_url.
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A dictionary containing mode, tempo, key, duration, time signature, loudness, danceability, energy and analysis_url keys.
            
        Example:
            >>> s = song.Song('SOGNMKX12B0B806320')
            >>> s.audio_summary
             {u'analysis_url': u'https://echonest-analysis.s3.amazonaws.com/TR/RnMKCg47J5LgQZr0SISyoPuRxKVQx3Z_YSuhVa/3/full.json?Signature=KBUbewLiP3sZ2X6rRZzXhrgh8fw%3D&Expires=1349809604&AWSAccessKeyId=AKIAJRDFEY23UEVW42BQ',
              u'audio_md5': u'ca3fdfa72eed23d5ad89872c38cecc0e',
              u'danceability': 0.33712086491871546,
              u'duration': 470.70666999999997,
              u'energy': 0.58186979146361684,
              u'key': 0,
              u'liveness': 0.08676759933615498,
              u'loudness': -9.5960000000000001,
              u'mode': 1,
              u'speechiness': 0.036938896635994867,
              u'tempo': 126.949,
              u'time_signature': 4}
            >>> 
            
        """
        if not (cache and ('audio_summary' in self.cache)):
            response = self.get_attribute('profile', bucket='audio_summary')
            if response['songs'] and 'audio_summary' in response['songs'][0]:
                self.cache['audio_summary'] = response['songs'][0]['audio_summary']
            else:
                self.cache['audio_summary'] = {}
        return self.cache['audio_summary']
    
    audio_summary = property(get_audio_summary)
    
    def get_song_hotttnesss(self, cache=True):
        """Get our numerical description of how hottt a song currently is
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing hotttnesss.
        
        Example:
            >>> s = song.Song('SOLUHKP129F0698D49')
            >>> s.get_song_hotttnesss()
            0.57344379999999995
            >>> s.song_hotttnesss
            0.57344379999999995
            >>> 

        """
        if not (cache and ('song_hotttnesss' in self.cache)):
            response = self.get_attribute('profile', bucket='song_hotttnesss')
            self.cache['song_hotttnesss'] = response['songs'][0]['song_hotttnesss']
        return self.cache['song_hotttnesss']
    
    song_hotttnesss = property(get_song_hotttnesss)

    def get_song_type(self, cache=True):
        """Get the types of a song.
        
        Args:
            cache (boolean): A boolean indicating whether or not the cached value should be used
            (if available). Defaults to True.
        
        Returns:
            A list of strings, each representing a song type:  'christmas', for example.
        
        Example:
            >>> s = song.Song('SOQKVPH12A58A7AF4D')
            >>> s.song_type
            [u'christmas']
            >>> 

        """ 
        if not (cache and ('song_type' in self.cache)):
            response = self.get_attribute('profile', bucket='song_type')
            if response['songs'][0].has_key('song_type'):
                self.cache['song_type'] = response['songs'][0]['song_type']
            else:
                self.cache['song_type'] = []
        return self.cache['song_type']

    song_type = property(get_song_type)
    
    def get_artist_hotttnesss(self, cache=True):
        """Get our numerical description of how hottt a song's artist currently is
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing hotttnesss.
        
        Example:
            >>> s = song.Song('SOOLGAZ127F3E1B87C')
            >>> s.artist_hotttnesss
            0.45645633000000002
            >>> s.get_artist_hotttnesss()
            0.45645633000000002
            >>> 
        
        """
        if not (cache and ('artist_hotttnesss' in self.cache)):
            response = self.get_attribute('profile', bucket='artist_hotttnesss')
            self.cache['artist_hotttnesss'] = response['songs'][0]['artist_hotttnesss']
        return self.cache['artist_hotttnesss']
    
    artist_hotttnesss = property(get_artist_hotttnesss)
    
    def get_artist_familiarity(self, cache=True):
        """Get our numerical estimation of how familiar a song's artist currently is to the world
        
        Args:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing familiarity.
        
        Example:
            >>> s = song.Song('SOQKVPH12A58A7AF4D')
            >>> s.get_artist_familiarity()
            0.639626025843539
            >>> s.artist_familiarity
            0.639626025843539
            >>> 
        """
        if not (cache and ('artist_familiarity' in self.cache)):
            response = self.get_attribute('profile', bucket='artist_familiarity')
            self.cache['artist_familiarity'] = response['songs'][0]['artist_familiarity']
        return self.cache['artist_familiarity']
    
    artist_familiarity = property(get_artist_familiarity)
    
    def get_artist_location(self, cache=True):
        """Get the location of a song's artist.
        
        Args:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            An artist location object.
        
        Example:
            >>> s = song.Song('SOQKVPH12A58A7AF4D')
            >>> s.artist_location
            {u'latitude': 34.053489999999996, u'location': u'Los Angeles, CA', u'longitude': -118.24532000000001}
            >>> 

        """
        if not (cache and ('artist_location' in self.cache)):
            response = self.get_attribute('profile', bucket='artist_location')
            self.cache['artist_location'] = response['songs'][0]['artist_location']
        return self.cache['artist_location']
    
    artist_location = property(get_artist_location)
    
    def get_foreign_id(self, idspace='', cache=True):
        """Get the foreign id for this song for a specific id space
        
        Args:
        
        Kwargs:
            idspace (str): A string indicating the idspace to fetch a foreign id for.
        
        Returns:
            A foreign ID string
        
        Example:
        
        >>> s = song.Song('SOYRVMR12AF729F8DC')
        >>> s.get_foreign_id('CAGPXKK12BB06F9DE9')
        
        >>> 
        """
        idspace = util.map_idspace(idspace)
        if not (cache and ('foreign_ids' in self.cache) and filter(lambda d: d.get('catalog') == idspace, self.cache['foreign_ids'])):
            response = self.get_attribute('profile', bucket=['id:'+idspace])
            rsongs = response['songs']
            if len(rsongs) == 0:
                return None
            foreign_ids = rsongs[0].get("foreign_ids", [])
            self.cache['foreign_ids'] = self.cache.get('foreign_ids', []) + foreign_ids
        cval = filter(lambda d: d.get('catalog') == idspace, self.cache.get('foreign_ids'))
        return cval[0].get('foreign_id') if cval else None

    def get_song_discovery(self, cache=True):
        """
        Args:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.

        Returns:
            A float representing a song's discovery rank.

        Example:
            >>> s = song.Song('SOQKVPH12A58A7AF4D')
            >>> s.get_song_discovery()
            0.639626025843539
            >>> s.song_discovery
            0.639626025843539
            >>>
        """
        if not (cache and ('song_discovery' in self.cache)):
            response = self.get_attribute('profile', bucket='song_discovery')
            self.cache['song_discovery'] = response['songs'][0]['song_discovery']
        return self.cache['song_discovery']

    song_discovery = property(get_song_discovery)

    def get_song_currency(self, cache=True):
        """
        Args:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing a song's currency rank.
            
        Example:
            >>> s = song.Song('SOQKVPH12A58A7AF4D')
            >>> s.get_song_currency()
            0.639626025843539
            >>> s.song_currency
            0.639626025843539
            >>>
        """
        if not (cache and ('song_currency' in self.cache)):
            response = self.get_attribute('profile', bucket='song_currency')
            self.cache['song_currency'] = response['songs'][0]['song_currency']
        return self.cache['song_currency']

    song_currency = property(get_song_currency)
    
    def get_tracks(self, catalog, cache=True):
        """Get the tracks for a song given a catalog.
        
        Args:
            catalog (str): a string representing the catalog whose track you want to retrieve.
        
        Returns:
            A list of Track dicts.
        
        Example:
            >>> s = song.Song('SOWDASQ12A6310F24F')
            >>> s.get_tracks('7digital')[0]
            {u'catalog': u'7digital',
             u'foreign_id': u'7digital:track:8445818',
             u'id': u'TRJGNNY12903CC625C',
             u'preview_url': u'http://previews.7digital.com/clips/34/8445818.clip.mp3',
             u'release_image': u'http://cdn.7static.com/static/img/sleeveart/00/007/628/0000762838_200.jpg'}
            >>> 

        """
        if not (cache and ('tracks' in self.cache) and (catalog in [td['catalog'] for td in self.cache['tracks']])):
            kwargs = {
                'bucket':['tracks', 'id:%s' % catalog],
            }
                        
            response = self.get_attribute('profile', **kwargs)
            if not 'tracks' in self.cache:
                self.cache['tracks'] = []
            # don't blow away the cache for other catalogs
            potential_tracks = response['songs'][0].get('tracks', [])
            existing_track_ids = [tr['foreign_id'] for tr in self.cache['tracks']]
            new_tds = filter(lambda tr: tr['foreign_id'] not in existing_track_ids, potential_tracks)
            self.cache['tracks'].extend(new_tds)
        return filter(lambda tr: tr['catalog']==util.map_idspace(catalog), self.cache['tracks'])


def search(title=None, artist=None, artist_id=None, combined=None, description=None, style=None, mood=None,
           results=None, start=None, max_tempo=None, min_tempo=None,
           max_duration=None, min_duration=None, max_loudness=None, min_loudness=None,
           artist_max_familiarity=None, artist_min_familiarity=None, artist_max_hotttnesss=None,
           artist_min_hotttnesss=None, song_max_hotttnesss=None, song_min_hotttnesss=None, mode=None,
           min_energy=None, max_energy=None, min_danceability=None, max_danceability=None,
           key=None, max_latitude=None, min_latitude=None, max_longitude=None, min_longitude=None,
           sort=None, buckets=None, limit=False, test_new_things=None, rank_type=None,
           artist_start_year_after=None, artist_start_year_before=None, artist_end_year_after=None,
           artist_end_year_before=None,song_type=None,min_song_currency=None,max_song_currency=None,
           min_song_discovery=None, max_song_discovery=None, max_acousticness=None, min_acousticness=None,
           max_liveness=None, min_liveness=None, max_speechiness=None, min_speechiness=None,
           max_valence=None, min_valence=None):
    """Search for songs by name, description, or constraint.

    Args:

    Kwargs:
        title (str): the name of a song
        artist (str): the name of an artist
        artist_id (str): the artist_id
        combined (str): the artist name and song title
        description (str): A string describing the artist and song
        style (str): A string describing the style/genre of the artist and song
        mood (str): A string describing the mood of the artist and song
        results (int): An integer number of results to return
        max_acousticness (float): The max acousticness of song results
        min_acousticness (float): The min acousticness of song results
        max_tempo (float): The max tempo of song results
        min_tempo (float): The min tempo of song results
        max_duration (float): The max duration of song results
        min_duration (float): The min duration of song results
        max_liveness (float): The max liveness of song results
        min_liveness (float): The min liveness of song results
        max_loudness (float): The max loudness of song results
        min_loudness (float): The min loudness of song results
        max_speechiness (float): The max speechiness of song results        
        min_speechiess (float): The min speechiness of song results
        max_valence (float): The max valence of song results
        min_valence (float): The min valence of song results
        artist_max_familiarity (float): A float specifying the max familiarity of artists to search for
        artist_min_familiarity (float): A float specifying the min familiarity of artists to search for
        artist_max_hotttnesss (float): A float specifying the max hotttnesss of artists to search for
        artist_min_hotttnesss (float): A float specifying the max hotttnesss of artists to search for
        song_max_hotttnesss (float): A float specifying the max hotttnesss of songs to search for
        song_min_hotttnesss (float): A float specifying the max hotttnesss of songs to search for
        max_energy (float): The max energy of song results
        min_energy (float): The min energy of song results
        max_dancibility (float): The max dancibility of song results
        min_dancibility (float): The min dancibility of song results
        mode (int): 0 or 1 (minor or major)
        key (int): 0-11 (c, c-sharp, d, e-flat, e, f, f-sharp, g, a-flat, a, b-flat, b)
        max_latitude (float): A float specifying the max latitude of artists to search for
        min_latitude (float): A float specifying the min latitude of artists to search for
        max_longitude (float): A float specifying the max longitude of artists to search for
        min_longitude (float): A float specifying the min longitude of artists to search for                        
        sort (str): A string indicating an attribute and order for sorting the results
        buckets (list): A list of strings specifying which buckets to retrieve
        limit (bool): A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
        rank_type (str): A string denoting the desired ranking for description searches, either 'relevance' or 'familiarity
        artist_start_year_before (int): Returned songs's artists will have started recording music before this year.
        artist_start_year_after (int): Returned songs's artists will have started recording music after this year.
        artist_end_year_before (int): Returned songs's artists will have stopped recording music before this year.
        artist_end_year_after (int): Returned songs's artists will have stopped recording music after this year.
        song_type (string): A string or list of strings specifiying the type of song to search for.

    Returns:
        A list of Song objects

    Example:

    >>> results = song.search(artist='shakira', title='she wolf', buckets=['id:7digital', 'tracks'], limit=True, results=1)
    >>> results
    [<song - She Wolf>]
    >>> results[0].get_tracks('7digital')[0]
    {u'catalog': u'7digital',
     u'foreign_id': u'7digital:track:7854109',
     u'id': u'TRTOBSE12903CACEC4',
     u'preview_url': u'http://previews.7digital.com/clips/34/7854109.clip.mp3',
     u'release_image': u'http://cdn.7static.com/static/img/sleeveart/00/007/081/0000708184_200.jpg'}
    >>> 
    """
    
    limit = str(limit).lower()
    kwargs = locals()
    kwargs['bucket'] = buckets
    del kwargs['buckets']
    
    result = util.callm("%s/%s" % ('song', 'search'), kwargs)
    return [Song(**util.fix(s_dict)) for s_dict in result['response']['songs']]

def profile(ids=None, track_ids=None, buckets=None, limit=False):
    """get the profiles for multiple songs at once
        
    Args:
        ids (str or list): a song ID or list of song IDs
    
    Kwargs:
        buckets (list): A list of strings specifying which buckets to retrieve

        limit (bool): A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
    
    Returns:
        A list of term document dicts
    
    Example:

    >>> song_ids = ['SOBSLVH12A8C131F38', 'SOXMSGY1338A5D5873', 'SOJPHZO1376210AFE5', 'SOBHNKR12AB0186218', 'SOSJAHD13770F4D40C']
    >>> songs = song.profile(song_ids, buckets=['audio_summary'])
    [<song - Say It Ain't So>,
     <song - Island In The Sun>,
     <song - My Name Is Jonas>,
     <song - Buddy Holly>]
    >>> songs[0].audio_summary
    {u'analysis_url': u'https://echonest-analysis.s3.amazonaws.com/TR/7VRBNguufpHAQQ4ZjJ0eWsIQWl2S2_lrK-7Bp2azHOvPN4VFV-YnU7uO0dXgYtOKT-MTEa/3/full.json?Signature=hmNghHwfEsA4JKWFXnRi7mVP6T8%3D&Expires=1349809918&AWSAccessKeyId=AKIAJRDFEY23UEVW42BQ',
     u'audio_md5': u'b6079b2b88f8265be8bdd5fe9702e05c',
     u'danceability': 0.64540643050283253,
     u'duration': 255.92117999999999,
     u'energy': 0.30711665772260549,
     u'key': 8,
     u'liveness': 0.088994423525370583,
     u'loudness': -9.7799999999999994,
     u'mode': 1,
     u'speechiness': 0.031970700260699259,
     u'tempo': 76.049999999999997,
     u'time_signature': 4}
    >>> 
    """
    kwargs = {}

    if ids:
        if not isinstance(ids, list):
            ids = [ids]
        kwargs['id'] = ids

    if track_ids:
        if not isinstance(track_ids, list):
            track_ids = [track_ids]
        kwargs['track_id'] = track_ids

    buckets = buckets or []
    if buckets:
        kwargs['bucket'] = buckets

    if limit:
        kwargs['limit'] = 'true'
    
    result = util.callm("%s/%s" % ('song', 'profile'), kwargs)
    return [Song(**util.fix(s_dict)) for s_dict in result['response']['songs']]

