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
import catalog

class Playlist(PlaylistProxy):
    """
    A Dynamic Playlist object
    
    Attributes:
        session_id (str): Playlist Session ID

        song (song object): The current song

        info (dictionary): Information about this playlist
    
    Example:
        >>> p = Playlist(type='artist-radio', artist=['ida maria', 'florence + the machine'])
        >>> p
        <Dynamic Playlist - 9c210205d4784144b4fa90770fa55d0b>
        >>> p.song
        <song - Later On>
        >>> p.get_next_song()
        <song - Overall>
        >>> 

    """
    
    def __init__(self, session_id=None, type='artist', artist_pick='song_hotttnesss-desc', variety=.5, artist_id=None, artist=None, \
                        song_id=None, track_id=None, description=None, style=None, mood=None, \
                        max_tempo=None, min_tempo=None, max_duration=None, \
                        min_duration=None, max_loudness=None, min_loudness=None, max_danceability=None, min_danceability=None, \
                        max_energy=None, min_energy=None, artist_max_familiarity=None, artist_min_familiarity=None, \
                        artist_max_hotttnesss=None, artist_min_hotttnesss=None, song_max_hotttnesss=None, song_min_hotttnesss=None, \
                        min_longitude=None, max_longitude=None, min_latitude=None, max_latitude=None, adventurousness=0.2, \
                        mode=None, key=None, buckets=[], sort=None, limit=False, 
                        dmca=False, chain_xspf=False, \
                        seed_catalog=None, steer=None, source_catalog=None, steer_description=None, test_new_things=None, rank_type=None,
                        artist_start_year_after=None, artist_start_year_before=None, artist_end_year_after=None, artist_end_year_before=None):
        """
        Args:

        Kwargs:
            type (str): a string representing the playlist type ('artist', 'artist-radio', ...)

            artist_pick (str): How songs should be chosen for each artist

            variety (float): A number between 0 and 1 specifying the variety of the playlist

            artist_id (str): the artist_id

            artist (str): the name of an artist

            song_id (str): the song_id

            track_id (str): the track_id

            description (str): A string describing the artist and song
            
            style (str): A string describing the style/genre of the artist and song

            mood (str): A string describing the mood of the artist and song
            
            results (int): An integer number of results to return

            max_tempo (float): The max tempo of song results

            min_tempo (float): The min tempo of song results

            max_duration (float): The max duration of song results

            min_duration (float): The min duration of song results

            max_loudness (float): The max loudness of song results

            min_loudness (float): The min loudness of song results

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

            adventurousness (float): A float ranging from 0 for old favorites to 1.0 for unheard music according to a seed_catalog

            sort (str): A string indicating an attribute and order for sorting the results

            buckets (list): A list of strings specifying which buckets to retrieve

            limit (bool): A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets

            seed_catalog (str or Catalog): A Catalog object or catalog id to use as a seed
            
            source_catalog (str or Catalog): A Catalog object or catalog id
            
            steer (str): A steering value to determine the target song attributes
            
            steer_description (str): A steering value to determine the target song description term attributes
            
            rank_type (str): A string denoting the desired ranking for description searches, either 'relevance' or 'familiarity'
            
            artist_start_year_before (int): Returned songs's artists will have started recording music before this year.
            
            artist_start_year_after (int): Returned songs's artists will have started recording music after this year.
            
            artist_end_year_before (int): Returned songs's artists will have stopped recording music before this year.
            
            artist_end_year_after (int): Returned songs's artists will have stopped recording music after this year.
            
        Returns:
            A dynamic playlist object
        
            
        """
        limit = str(limit).lower()
        dmca = str(dmca).lower()
        chain_xspf = str(chain_xspf).lower()
        
        if isinstance(seed_catalog, catalog.Catalog):
            seed_catalog = seed_catalog.id

        if isinstance(source_catalog, catalog.Catalog):
            source_catalog = source_catalog.id

        kwargs = locals()
        kwargs['bucket'] = kwargs['buckets']
        del kwargs['buckets']
        del kwargs['self']
        del kwargs['session_id']
        
        super(Playlist, self).__init__(session_id, **kwargs)
    
    def __repr__(self):
        return "<Dynamic Playlist - %s>" % self.session_id.encode('utf-8')
    
    # def __str__(self):
    #     return self.name.encode('utf-8')
    
    def get_next_song(self, **kwargs):
        """Get the next song in the playlist
        
        Args:
        
        Kwargs:
        
        Returns:
            A song object
        
        Example:
        
        >>> p = playlist.Playlist(type='artist-radio', artist=['ida maria', 'florence + the machine'])
        >>> p.get_next_song()
        <song - She Said>
        >>>
        
        """
        response = self.get_attribute('dynamic', session_id=self.session_id, **kwargs)
        self.cache['songs'] = response['songs']
        # we need this to fix up all the dict keys to be strings, not unicode objects
        fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
        if len(self.cache['songs']):
            return Song(**fix(self.cache['songs'][0]))
        else:
            return None
    
    def get_current_song(self):
        """Get the current song in the playlist
        
        Args:
        
        Kwargs:
        
        Returns:
            A song object
        
        Example:
        
        >>> p = playlist.Playlist(type='artist-radio', artist=['ida maria', 'florence + the machine'])
        >>> p.song
        <song - Later On>
        >>> p.get_current_song()
        <song - Later On>
        >>> 

        """
        # we need this to fix up all the dict keys to be strings, not unicode objects
        if not 'songs' in self.cache:
            self.get_next_song()
        if len(self.cache['songs']):
            return Song(**util.fix(self.cache['songs'][0]))
        else:
            return None

    song = property(get_current_song)
    
    def session_info(self):
        """Get information about the playlist
        
        Args:
        
        Kwargs:
        
        Returns:
            A dict with diagnostic information about the currently running playlist
        
        Example:
        
        >>> p = playlist.Playlist(type='artist-radio', artist=['ida maria', 'florence + the machine'])
        >>> p.info
        {
            u 'terms': [{
                u 'frequency': 1.0,
                u 'name': u 'rock'
            },
            {
                u 'frequency': 0.99646542152360207,
                u 'name': u 'pop'
            },
            {
                u 'frequency': 0.90801905502131963,
                u 'name': u 'indie'
            },
            {
                u 'frequency': 0.90586455490260576,
                u 'name': u 'indie rock'
            },
            {
                u 'frequency': 0.8968907243373172,
                u 'name': u 'alternative'
            },
            [...]
            {
                u 'frequency': 0.052197425644931635,
                u 'name': u 'easy listening'
            }],
            u 'description': [],
            u 'seed_songs': [],
            u 'banned_artists': [],
            u 'rules': [{
                u 'rule': u "Don't put two copies of the same song in a playlist."
            },
            {
                u 'rule': u 'Give preference to artists that are not already in the playlist'
            }],
            u 'session_id': u '9c1893e6ace04c8f9ce745f38b35ff95',
            u 'seeds': [u 'ARI4XHX1187B9A1216', u 'ARNCHOP121318C56B8'],
            u 'skipped_songs': [],
            u 'banned_songs': [],
            u 'playlist_type': u 'artist-radio',
            u 'seed_catalogs': [],
            u 'rated_songs': [],
            u 'history': [{
                u 'artist_id': u 'ARN6QMG1187FB56C8D',
                u 'artist_name': u 'Laura Marling',
                u 'id': u 'SOMSHNP12AB018513F',
                u 'served_time': 1291412277.204201,
                u 'title': u 'Hope In The Air'
            }]
        }
        
        >>> p.session_info()
        (same result as above)
        >>> 

        """
        return self.get_attribute("session_info", session_id=self.session_id)
    
    info = property(session_info)


def basic(type='artist-radio', artist_id=None, artist=None, song_id=None, song=None, track_id=None,
          dmca=False, results=15, buckets=None, limit=False):
    """Get a basic playlist
    
    Args:
    
    Kwargs:
        type (str): a string representing the playlist type ('artist-radio' or 'song-radio')
        
        artist_id (str): the artist_id to seed the playlist
        
        artist (str): the name of an artist to seed the playlist
        
        song_id (str): a song_id to seed the playlist
        
        song (str): the name of a song to seed the playlist
        
        track_id (str): the name of a track to seed the playlist
        
        dmca (bool): make the playlist dmca-compliant
        
        results (int): desired length of the playlist
        
        buckets (list): A list of strings specifying which buckets to retrieve
        
        limit (bool): Whether results should be restricted to any idspaces given in the buckets parameter
    """
    
    limit = str(limit).lower()
    dmca = str(dmca).lower()
    
    kwargs = locals()
    kwargs['bucket'] = kwargs['buckets']
    del kwargs['buckets']
    
    result = util.callm("%s/%s" % ('playlist', 'basic'), kwargs)
    return [Song(**util.fix(s_dict)) for s_dict in result['response']['songs']]    


def static(type='artist', artist_pick='song_hotttnesss-desc', variety=.5, artist_id=None, artist=None, \
                    song_id=None, track_id=None, description=None, style=None, mood=None, \
                    results=15, max_tempo=None, min_tempo=None, max_duration=None, \
                    min_duration=None, max_loudness=None, min_loudness=None, max_danceability=None, min_danceability=None, \
                    max_energy=None, min_energy=None, artist_max_familiarity=None, artist_min_familiarity=None, \
                    artist_max_hotttnesss=None, artist_min_hotttnesss=None, song_max_hotttnesss=None, song_min_hotttnesss=None, \
                    min_longitude=None, max_longitude=None, min_latitude=None, max_latitude=None, adventurousness=0.2, \
                    mode=None, key=None, buckets=[], sort=None, limit=False, seed_catalog=None, source_catalog=None, rank_type=None, test_new_things=None,
                    artist_start_year_after=None, artist_start_year_before=None, artist_end_year_after=None, artist_end_year_before=None,dmca=False):
    """Get a static playlist
    
    Args:
    
    Kwargs:
        type (str): a string representing the playlist type ('artist', 'artist-radio', ...)
        
        artist_pick (str): How songs should be chosen for each artist
        
        variety (float): A number between 0 and 1 specifying the variety of the playlist
        
        artist_id (str): the artist_id
        
        artist (str): the name of an artist
        
        song_id (str): the song_id
        
        track_id (str): the track id
        
        description (str): A string describing the artist and song
        
        style (str): A string describing the style/genre of the artist and song
    
        mood (str): A string describing the mood of the artist and song
        
        results (int): An integer number of results to return
    
        max_tempo (float): The max tempo of song results
    
        min_tempo (float): The min tempo of song results
    
        max_duration (float): The max duration of song results
    
        min_duration (float): The min duration of song results
    
        max_loudness (float): The max loudness of song results
    
        min_loudness (float): The min loudness of song results
    
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
        
        adventurousness (float): A float ranging from 0 for old favorites to 1.0 for unheard music according to a seed_catalog
    
        sort (str): A string indicating an attribute and order for sorting the results
    
        buckets (list): A list of strings specifying which buckets to retrieve
    
        limit (bool): A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
        
        seed_catalog (str or Catalog): An Artist Catalog object or Artist Catalog id to use as a seed
        
        source_catalog (str or Catalog): A Catalog object or catalog id

        rank_type (str): A string denoting the desired ranking for description searches, either 'relevance' or 'familiarity'    
        
        artist_start_year_before (int): Returned songs's artists will have started recording music before this year.
        
        artist_start_year_after (int): Returned songs's artists will have started recording music after this year.
        
        artist_end_year_before (int): Returned songs's artists will have stopped recording music before this year.
        
        artist_end_year_after (int): Returned songs's artists will have stopped recording music after this year.

    Returns:
        A list of Song objects
    
    Example:
    
    >>> p = playlist.static(type='artist-radio', artist=['ida maria', 'florence + the machine'])
    >>> p
    [<song - Pickpocket>,
     <song - Self-Taught Learner>,
     <song - Maps>,
     <song - Window Blues>,
     <song - That's Not My Name>,
     <song - My Lover Will Go>,
     <song - Home Sweet Home>,
     <song - Stella & God>,
     <song - Don't You Want To Share The Guilt?>,
     <song - Forget About It>,
     <song - Dull Life>,
     <song - This Trumpet In My Head>,
     <song - Keep Your Head>,
     <song - One More Time>,
     <song - Knights in Mountain Fox Jackets>]
    >>> 

    """
    limit = str(limit).lower()

    if seed_catalog and isinstance(seed_catalog, catalog.Catalog):
        seed_catalog = seed_catalog.id

    if source_catalog and isinstance(source_catalog, catalog.Catalog):
        source_catalog = source_catalog.id
    dmca = str(dmca).lower()
    kwargs = locals()
    kwargs['bucket'] = kwargs['buckets']
    del kwargs['buckets']
    
    result = util.callm("%s/%s" % ('playlist', 'static'), kwargs)
    return [Song(**util.fix(s_dict)) for s_dict in result['response']['songs']]
