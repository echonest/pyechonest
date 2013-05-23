#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import logging
logger = logging.getLogger(__name__)


def basic(type='artist-radio', artist_id=None, artist=None, song_id=None, song=None, track_id=None, dmca=False,
          results=15, buckets=None, limit=False,genres=None,):
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
    kwargs['genre'] = kwargs['genres']
    del kwargs['genres']

    result = util.callm("%s/%s" % ('playlist', 'basic'), kwargs)
    return [Song(**util.fix(s_dict)) for s_dict in result['response']['songs']]


def static(type='artist', artist_pick='song_hotttnesss-desc', variety=.5, artist_id=None, artist=None, song_id=None,
           track_id=None, description=None, style=None, mood=None, results=15, max_tempo=None, min_tempo=None,
           max_duration=None, min_duration=None, max_loudness=None, min_loudness=None, max_danceability=None,
           min_danceability=None, max_energy=None, min_energy=None, artist_max_familiarity=None,
           artist_min_familiarity=None, artist_max_hotttnesss=None, artist_min_hotttnesss=None,
           song_max_hotttnesss=None, song_min_hotttnesss=None, min_longitude=None, max_longitude=None,
           min_latitude=None, max_latitude=None, adventurousness=0.2, mode=None, key=None, buckets=None, sort=None,
           limit=False, seed_catalog=None, source_catalog=None, rank_type=None, test_new_things=None,
           artist_start_year_after=None, artist_start_year_before=None, artist_end_year_after=None,
           artist_end_year_before=None, dmca=False, distribution=None, song_type=None, genres=None):
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
    
        max_danceability (float): The max danceability of song results
    
        min_danceability (float): The min danceability of song results
    
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
        
        artist_start_year_before (int): Returned song's artists will have started recording music before this year.
        
        artist_start_year_after (int): Returned song's artists will have started recording music after this year.
        
        artist_end_year_before (int): Returned song's artists will have stopped recording music before this year.
        
        artist_end_year_after (int): Returned song's artists will have stopped recording music after this year.

        distribution (str): Affects the range of artists returned and how many songs each artist will have in the playlist relative to how similar they are to the seed. (wandering, focused)

        song_type (str):  A string or list of strings of the type of songs allowed.  The only valid song type at the moment is 'christmas'.
                          Valid formats are 'song_type', 'song_type:true', 'song_type:false', or 'song_type:any'.

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
    kwargs['bucket'] = kwargs['buckets'] or []
    del kwargs['buckets']
    kwargs['genre'] = kwargs['genres']
    del kwargs['genres']

    result = util.callm("%s/%s" % ('playlist', 'static'), kwargs)
    return [Song(**util.fix(s_dict)) for s_dict in result['response']['songs']]

class Playlist(PlaylistProxy):
    """
    A Dynamic Playlist object.
    http://developer.echonest.com/docs/v4/playlist.html#dynamic-create

    Attributes:

    Example:
    """

    def __init__(
            self, session_id=None, type=None, artist_pick=None, variety=None, artist_id=None, artist=None, song_id=None,
            track_id=None, description=None, style=None, mood=None, max_tempo=None, min_tempo=None, max_duration=None,
            min_duration=None, max_loudness=None, min_loudness=None, max_danceability=None, min_danceability=None,
            max_energy=None, min_energy=None, artist_max_familiarity=None, artist_min_familiarity=None,
            artist_max_hotttnesss=None, artist_min_hotttnesss=None, song_max_hotttnesss=None, song_min_hotttnesss=None,
            min_longitude=None, max_longitude=None, min_latitude=None, max_latitude=None, adventurousness=None,
            mode=None, key=None, buckets=None, sort=None, limit=False, seed_catalog=None, source_catalog=None,
            rank_type=None, test_new_things=None, artist_start_year_after=None, artist_start_year_before=None,
            artist_end_year_after=None, artist_end_year_before=None, dmca=False, distribution=None, song_type=None,
            session_catalog=None,genres=None,):

        limit = str(limit).lower()
        dmca = str(dmca).lower()

        if isinstance(seed_catalog, catalog.Catalog):
            seed_catalog = seed_catalog.id

        super(Playlist, self).__init__(
            session_id=session_id,
            type=type,
            artist_pick=artist_pick,
            variety=variety,
            artist_id=artist_id,
            artist=artist,
            song_id=song_id,
            track_id=track_id,
            description=description,
            style=style,
            mood=mood,
            max_tempo=max_tempo,
            min_tempo=min_tempo,
            max_duration=max_duration,
            min_duration=min_duration,
            max_loudness=max_loudness,
            min_loudness=min_loudness,
            max_danceability=max_danceability,
            min_danceability=min_danceability,
            max_energy=max_energy,
            min_energy=min_energy,
            artist_max_familiarity=artist_max_familiarity,
            artist_min_familiarity=artist_min_familiarity,
            artist_max_hotttnesss=artist_max_hotttnesss,
            artist_min_hotttnesss=artist_min_hotttnesss,
            song_max_hotttnesss=song_max_hotttnesss,
            song_min_hotttnesss=song_min_hotttnesss,
            min_longitude=min_longitude,
            max_longitude=max_longitude,
            min_latitude=min_latitude,
            max_latitude=max_latitude,
            adventurousness=adventurousness,
            mode=mode,
            key=key,
            buckets=buckets,
            sort=sort,
            limit=limit,
            seed_catalog=seed_catalog,
            source_catalog=source_catalog,
            rank_type=rank_type,
            test_new_things=test_new_things,
            artist_start_year_after=artist_start_year_after,
            artist_start_year_before=artist_start_year_before,
            artist_end_year_after=artist_end_year_after,
            artist_end_year_before=artist_end_year_before,
            dmca=dmca,
            distribution=distribution,
            song_type=song_type,
            session_catalog=session_catalog,
            genres=genres
        )


    def __repr__(self):
        return "<Dynamic Playlist - %s>" % self.session_id.encode('utf-8')

    def get_next_songs(self, results=None, lookahead=None):
        response = self.get_attribute(
            method='next',
            session_id=self.session_id,
            results=results,
            lookahead=lookahead
        )
        self.cache['songs'] = response['songs']
        self.cache['lookahead'] = response['lookahead']
        if len(self.cache['songs']):
            songs = self.cache['songs'][:]
            songs = [Song(**util.fix(song)) for song in songs]
            return songs
        else:
            return None

    def get_current_songs(self):
        if not 'songs' in self.cache:
            self.get_next_songs(results=1)
        if len(self.cache['songs']):
            songs = self.cache['songs'][:]
            songs = [Song(**util.fix(song)) for song in songs]

            return songs
        else:
            return None

    def get_lookahead_songs(self):
        if not 'lookahead' in self.cache:
            return None
        if len(self.cache['lookahead']):
            lookahead = self.cache['lookahead'][:]
            lookahead = [Song(**util.fix(song)) for song in lookahead]

            return lookahead
        else:
            return None

    songs = property(get_current_songs)

    def info(self):
        return self.get_attribute("info", session_id=self.session_id)

    def delete(self):
        self.get_attribute("delete", session_id=self.session_id)
        return True

    def restart(
        self,
        type=None,
        artist_pick=None,
        variety=None,
        artist_id=None,
        artist=None,
        song_id=None,
        track_id=None,
        description=None,
        style=None,
        mood=None,
        max_tempo=None,
        min_tempo=None,
        max_duration=None,
        min_duration=None,
        max_loudness=None,
        min_loudness=None,
        max_danceability=None,
        min_danceability=None,
        max_energy=None,
        min_energy=None,
        artist_max_familiarity=None,
        artist_min_familiarity=None,
        artist_max_hotttnesss=None,
        artist_min_hotttnesss=None,
        song_max_hotttnesss=None,
        song_min_hotttnesss=None,
        min_longitude=None,
        max_longitude=None,
        min_latitude=None,
        max_latitude=None,
        adventurousness=None,
        mode=None,
        key=None,
        buckets=None,
        sort=None,
        limit=False,
        seed_catalog=None,
        source_catalog=None,
        rank_type=None,
        test_new_things=None,
        artist_start_year_after=None,
        artist_start_year_before=None,
        artist_end_year_after=None,
        artist_end_year_before=None,
        dmca=False,
        distribution=None,
        song_type=None,
        genres=None,
    ):
        limit = str(limit).lower()
        dmca = str(dmca).lower()

        if isinstance(seed_catalog, catalog.Catalog):
            seed_catalog = seed_catalog.id


        return self.get_attribute(
            method='restart',
            session_id=self.session_id,
            type=type,
            artist_pick=artist_pick,
            variety=variety,
            artist_id=artist_id,
            artist=artist,
            song_id=song_id,
            track_id=track_id,
            description=description,
            style=style,
            mood=mood,
            max_tempo=max_tempo,
            min_tempo=min_tempo,
            max_duration=max_duration,
            min_duration=min_duration,
            max_loudness=max_loudness,
            min_loudness=min_loudness,
            max_danceability=max_danceability,
            min_danceability=min_danceability,
            max_energy=max_energy,
            min_energy=min_energy,
            artist_max_familiarity=artist_max_familiarity,
            artist_min_familiarity=artist_min_familiarity,
            artist_max_hotttnesss=artist_max_hotttnesss,
            artist_min_hotttnesss=artist_min_hotttnesss,
            song_max_hotttnesss=song_max_hotttnesss,
            song_min_hotttnesss=song_min_hotttnesss,
            min_longitude=min_longitude,
            max_longitude=max_longitude,
            min_latitude=min_latitude,
            max_latitude=max_latitude,
            adventurousness=adventurousness,
            mode=mode,
            key=key,
            bucket=buckets,
            sort=sort,
            limit=limit,
            seed_catalog=seed_catalog,
            source_catalog=source_catalog,
            rank_type=rank_type,
            test_new_things=test_new_things,
            artist_start_year_after=artist_start_year_after,
            artist_start_year_before=artist_start_year_before,
            artist_end_year_after=artist_end_year_after,
            artist_end_year_before=artist_end_year_before,
            dmca=dmca,
            distribution=distribution,
            song_type=song_type,
            genres=genres,
        )

    def steer(
        self,
        max_tempo=None,
        min_tempo=None,
        target_tempo=None,
        max_duration=None,
        min_duration=None,
        target_duration=None,
        max_loudness=None,
        min_loudness=None,
        target_loudness=None,
        max_danceability=None,
        min_danceability=None,
        target_danceability=None,
        max_energy=None,
        min_energy=None,
        target_energy=None,
        max_artist_familiarity=None,
        min_artist_familiarity=None,
        target_artist_familiarity=None,
        max_artist_hotttnesss=None,
        min_artist_hotttnesss=None,
        target_artist_hotttnesss=None,
        max_song_hotttnesss=None,
        min_song_hotttnesss=None,
        target_song_hotttnesss=None,
        more_like_this=None,
        less_like_this=None,
        adventurousness=None,
        variety=None,
        description=None,
        style=None,
        mood=None,
        song_type=None,
        genres=None
        ):

        response = self.get_attribute(
            method='steer',
            session_id=self.session_id,
            max_tempo=max_tempo,
            min_tempo=min_tempo,
            target_tempo=target_tempo,
            max_duration=max_duration,
            min_duration=min_duration,
            target_duration=target_duration,
            max_loudness=max_loudness,
            min_loudness=min_loudness,
            target_loudness=target_loudness,
            max_danceability=max_danceability,
            min_danceability=min_danceability,
            target_danceability=target_danceability,
            max_energy=max_energy,
            min_energy=min_energy,
            target_energy=target_energy,
            max_artist_familiarity=max_artist_familiarity,
            min_artist_familiarity=min_artist_familiarity,
            target_artist_familiarity=target_artist_familiarity,
            max_artist_hotttnesss=max_artist_hotttnesss,
            min_artist_hotttnesss=min_artist_hotttnesss,
            target_artist_hotttnesss=target_artist_hotttnesss,
            max_song_hotttnesss=max_song_hotttnesss,
            min_song_hotttnesss=min_song_hotttnesss,
            target_song_hotttnesss=target_song_hotttnesss,
            more_like_this=more_like_this,
            less_like_this=less_like_this,
            adventurousness=adventurousness,
            variety=variety,
            description=description,
            style=style,
            mood=mood,
            song_type=song_type,
            genres=genres,
            )

        self.cache['lookahead'] = []
        return True

    def feedback(
        self,
        ban_artist=None,
        ban_song=None,
        skip_song=None,
        favorite_artist=None,
        favorite_song=None,
        play_song=None,
        unplay_song=None,
        rate_song=None,
        invalidate_song=None,
        invalidate_artist=None,
        ):

        response = self.get_attribute(
            session_id=self.session_id,
            method='feedback',
            ban_artist=ban_artist,
            ban_song=ban_song,
            skip_song=skip_song,
            favorite_artist=favorite_artist,
            favorite_song=favorite_song,
            play_song=play_song,
            unplay_song=unplay_song,
            rate_song=rate_song,
            invalidate_song=invalidate_song,
            invalidate_artist=invalidate_artist,
            )

        self.cache['lookahead'] = []
        return True

class DeprecationHelper(object):

    def __init__(self, new_target):
        self.new_target = new_target

    def _warn(self):
        from warnings import warn
        warn("BetaPlaylist is no longer in Beta and has been moved to Playlist", DeprecationWarning, stacklevel=2)
        logger.warn("BetaPlaylist is no longer in Beta and has been moved to Playlist")

    def __call__(self, *args, **kwargs):
        self._warn()
        return self.new_target(*args, **kwargs)

    def __getattr__(self, attr):
        self._warn()
        return getattr(self.new_target, attr)

BetaPlaylist = DeprecationHelper(Playlist)
