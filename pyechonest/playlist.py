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
        session_id: Playlist Session ID
        song: The current song
    
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
                        song_id=None, description=None, max_tempo=None, min_tempo=None, max_duration=None, \
                        min_duration=None, max_loudness=None, min_loudness=None, max_danceability=None, min_danceability=None, \
                        max_energy=None, min_energy=None, artist_max_familiarity=None, artist_min_familiarity=None, \
                        artist_max_hotttnesss=None, artist_min_hotttnesss=None, song_max_hotttnesss=None, song_min_hotttnesss=None, \
                        min_longitude=None, max_longitude=None, min_latitude=None, max_latitude=None, \
                        mode=None, key=None, buckets=[], sort=None, limit=False, dmca=False, audio=False, chain_xspf=False, \
                        seed_catalog=None, steer=None, source_catalog=None, steer_description=None):
        """
        Args:

        Kwargs:
            type (str): a string representing the playlist type ('artist', 'artist-radio', ...)

            artist_pick (str): How songs should be chosen for each artist

            variety (float): A number between 0 and 1 specifying the variety of the playlist

            artist_id (str): the artist_id

            artist (str): the name of an artist

            song_id (str): the song_id

            description (str): A string describing the artist and song

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

            sort (str): A string indicating an attribute and order for sorting the results

            buckets (list): A list of strings specifying which buckets to retrieve

            limit (bool): A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets

            seed_catalog (str or Catalog): A Catalog object or catalog id to use as a seed
            
            source_catalog (str or Catalog): A Catalog object or catalog id
            
            steer (str): A steering value to determine the target song attributes
            
            steer_description (str): A steering value to determine the target song description term attributes
            
        
        Returns:
            A dynamic playlist object
        
            
        """
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
        if max_danceability is not None:
            kwargs['max_danceability'] = max_danceability
        if min_danceability is not None:
            kwargs['min_danceability'] = min_danceability
        if max_energy is not None:
            kwargs['max_energy'] = max_energy
        if min_energy is not None:
            kwargs['min_energy'] = min_energy
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
        if steer:
            kwargs['steer'] = steer
        if steer_description:
            kwargs['steer_description'] = steer_description
        if seed_catalog:
            if isinstance(seed_catalog, catalog.Catalog):
                kwargs['seed_catalog'] = seed_catalog.id
            else:
                kwargs['seed_catalog'] = seed_catalog
        if source_catalog:
            if isinstance(source_catalog, catalog.Catalog):
                kwargs['source_catalog'] = source_catalog.id
            else:
                kwargs['source_catalog'] = source_catalog
                        
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
        >>> p.session_info()
        {'banned_artists': [],
        'banned_songs': [],
        'description': [],
        'history': [{'artist_id': 'ARLBTH21187FB53191',
              'artist_name': 'The Ting Tings',
              'id': 'SOWCBXM12B0B80B9AA',
              'served_time': 1299092027.609634,
              'title': 'Impacilla Carpisung'}],
        'playlist_type': 'artist-radio',
        'rated_songs': [],
        'rules': [{'rule': "Don't put two copies of the same song in a playlist."},
           {'rule': 'Give preference to artists that are not already in the playlist'}],
        'seed_catalogs': [],
        'seed_songs': [],
        'seeds': ['ARI4XHX1187B9A1216', 'ARNCHOP121318C56B8'],
        'session_id': 'c71d718b2e854ec58ab76a72ec738fac',
        'skipped_songs': [],
        'terms': [{'frequency': 1.0, 'name': 'rock'},
           {'frequency': 0.9710461446720426, 'name': 'pop'},
           {'frequency': 0.8939321026174193, 'name': 'indie'},
           {'frequency': 0.8932392554185119, 'name': 'indie rock'},
           {'frequency': 0.7833920377163979, 'name': 'alternative'},
           {'frequency': 0.6503219368346062, 'name': 'alternative rock'},
           {'frequency': 0.6299762436483861, 'name': 'electronic'},
           {'frequency': 0.6111026978281094, 'name': 'indie pop'},
           {'frequency': 0.4174929087066686, 'name': 'acoustic'},
           {'frequency': 0.3804589191503101, 'name': 'electro'},
           {'frequency': 0.3528832098937301, 'name': 'punk'},
           {'frequency': 0.3477176570127335, 'name': 'folk'},
           {'frequency': 0.34438857004724255, 'name': 'pop rock'},
           {'frequency': 0.3201350993772201, 'name': 'female vocalist'},
           {'frequency': 0.2930136812912544, 'name': 'singer-songwriter'},
           {'frequency': 0.27855773620918817, 'name': 'guitar'},
           {'frequency': 0.2608897298026231, 'name': 'female'},
           {'frequency': 0.2257987517979643, 'name': 'jazz'},
           {'frequency': 0.22076257097805616, 'name': 'new wave'},
           {'frequency': 0.22067158583565338, 'name': 'experimental'},
           {'frequency': 0.22046269833131954, 'name': 'folk rock'},
           {'frequency': 0.2174644407782195, 'name': 'hip hop'},
           {'frequency': 0.20640617807458408, 'name': 'electronica'},
           {'frequency': 0.18755554090621548, 'name': 'vocal'},
           {'frequency': 0.18591926305314618, 'name': 'synthpop'},
           {'frequency': 0.18517407203199862, 'name': 'beautiful'},
           {'frequency': 0.18402101677161792, 'name': 'soft rock'},
           {'frequency': 0.16483655023966767, 'name': 'soundtrack'},
           {'frequency': 0.1620391620224837, 'name': '00s'},
           {'frequency': 0.1605208952456391, 'name': 'blues'},
           {'frequency': 0.15112621997644843, 'name': 'norwegian'},
           {'frequency': 0.15008765013390823, 'name': 'downtempo'},
           {'frequency': 0.1459932432706328, 'name': 'garage rock'},
           {'frequency': 0.14070914626164588, 'name': 'norway'},
           {'frequency': 0.1347077821207766, 'name': 'scandinavia'},
           {'frequency': 0.1335692053607083, 'name': 'mellow'},
           {'frequency': 0.12979468413175474, 'name': 'soul'},
           {'frequency': 0.12813192946395321, 'name': 'hard rock'},
           {'frequency': 0.12641809523587832, 'name': 'classic rock'},
           {'frequency': 0.12296650798160765, 'name': 'country rock'},
           {'frequency': 0.1213771466612416, 'name': 'piano'},
           {'frequency': 0.12076595580361003, 'name': 'post rock'},
           {'frequency': 0.11915721061731957, 'name': '80s'},
           {'frequency': 0.1110037740585051, 'name': 'ska'},
           {'frequency': 0.10883656693952001, 'name': 'house'},
           {'frequency': 0.1059204996140825, 'name': 'disco'},
           {'frequency': 0.10277729388723868, 'name': 'chill-out'},
           {'frequency': 0.09734141430337241, 'name': 'sweden'},
           {'frequency': 0.0952557930918705, 'name': 'pop rap'},
           {'frequency': 0.09445325509706426, 'name': 'emo'},
           {'frequency': 0.09376612792746737, 'name': 'europop'},
           {'frequency': 0.09218150809866822, 'name': 'female vocals'},
           {'frequency': 0.09198221711464794, 'name': 'ballad'},
           {'frequency': 0.09065007085811173, 'name': 'dream pop'},
           {'frequency': 0.09049064169015415, 'name': 'future jazz'},
           {'frequency': 0.08682614323719472, 'name': 'twee pop'},
           {'frequency': 0.08659366733188904, 'name': 'power pop'},
           {'frequency': 0.08585522015994426, 'name': 'swedish'},
           {'frequency': 0.08250832612424043, 'name': 'reggae'},
           {'frequency': 0.07974370431126251, 'name': 'dance pop'},
           {'frequency': 0.07946569653610241, 'name': 'country'},
           {'frequency': 0.07930367586262467, 'name': 'synth'},
           {'frequency': 0.07871897935547836, 'name': 'indietronica'},
           {'frequency': 0.07855152775656872, 'name': 'ambient'},
           {'frequency': 0.07610981138554565, 'name': 'heavy metal'},
           {'frequency': 0.07330890539699389, 'name': 'metal'},
           {'frequency': 0.07193010126455535, 'name': 'hardcore'},
           {'frequency': 0.06972580993314947, 'name': 'blues-rock'},
           {'frequency': 0.0696586262870633, 'name': 'psychedelic rock'},
           {'frequency': 0.06926151300222266, 'name': 'acid jazz'},
           {'frequency': 0.06807873571076452, 'name': 'progressive rock'},
           {'frequency': 0.06511658482129272, 'name': 'british'},
           {'frequency': 0.06468627727708089, 'name': 'melodic'},
           {'frequency': 0.06438061465050399, 'name': 'techno'},
           {'frequency': 0.0639721791940246, 'name': 'american'},
           {'frequency': 0.06313664884845813, 'name': 'england'},
           {'frequency': 0.06223616131680611, 'name': 'sexy'},
           {'frequency': 0.06199094786837033, 'name': 'soft'},
           {'frequency': 0.06196367416672277, 'name': 'alternative dance'},
           {'frequency': 0.060299115882783645, 'name': 'dark'},
           {'frequency': 0.060142917341880785, 'name': 'london'},
           {'frequency': 0.05862581739985387, 'name': 'song writer'},
           {'frequency': 0.058307539362263655, 'name': 'psychedelic'},
           {'frequency': 0.058297478633972666, 'name': 'shoegaze'},
           {'frequency': 0.056650664064182565, 'name': 'male vocalist'},
           {'frequency': 0.05563227271149839, 'name': 'funny'},
           {'frequency': 0.055121468530633794, 'name': 'melancholia'},
           {'frequency': 0.05483433641209914, 'name': 'british pop'},
           {'frequency': 0.05374448195920263, 'name': 'garage'},
           {'frequency': 0.05314211784143759, 'name': 'stoner rock'},
           {'frequency': 0.052948125820119575, 'name': 'dance'},
           {'frequency': 0.051924607548012584, 'name': 'tech house'},
           {'frequency': 0.05126270846286737, 'name': 'germany'},
           {'frequency': 0.05119529485602058, 'name': 'classical'},
           {'frequency': 0.05091457971841325, 'name': 'art rock'},
           {'frequency': 0.05003865991176611, 'name': 'european'},
           {'frequency': 0.04944584014487098, 'name': 'chanson'},
           {'frequency': 0.04844414853332869, 'name': 'dub'},
           {'frequency': 0.047419886407436905, 'name': 'black metal'},
           {'frequency': 0.04717140720623312, 'name': 'grunge'}]}
        >>> 

        """
        return self.get_attribute("session_info", session_id=self.session_id)
    
    info = property(session_info)


def static(type='artist', artist_pick='song_hotttnesss-desc', variety=.5, artist_id=None, artist=None, \
                    song_id=None, description=None, results=15, max_tempo=None, min_tempo=None, max_duration=None, \
                    min_duration=None, max_loudness=None, min_loudness=None, max_danceability=None, min_danceability=None, \
                    max_energy=None, min_energy=None, artist_max_familiarity=None, artist_min_familiarity=None, \
                    artist_max_hotttnesss=None, artist_min_hotttnesss=None, song_max_hotttnesss=None, song_min_hotttnesss=None, \
                    min_longitude=None, max_longitude=None, min_latitude=None, max_latitude=None, \
                    mode=None, key=None, buckets=[], sort=None, limit=False, seed_catalog=None, source_catalog=None):
    """Get a static playlist
    
    Args:
    
    Kwargs:
        type (str): a string representing the playlist type ('artist', 'artist-radio', ...)
        
        artist_pick (str): How songs should be chosen for each artist
        
        variety (float): A number between 0 and 1 specifying the variety of the playlist
        
        artist_id (str): the artist_id
        
        artist (str): the name of an artist
        
        song_id (str): the song_id
    
        description (str): A string describing the artist and song
    
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
    
        sort (str): A string indicating an attribute and order for sorting the results
    
        buckets (list): A list of strings specifying which buckets to retrieve
    
        limit (bool): A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
        
        seed_catalog (str or Catalog): An Artist Catalog object or Artist Catalog id to use as a seed
        
        source_catalog (str or Catalog): A Catalog object or catalog id
    
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
    if max_danceability is not None:
        kwargs['max_danceability'] = max_danceability
    if min_danceability is not None:
        kwargs['min_danceability'] = min_danceability
    if max_energy is not None:
        kwargs['max_energy'] = max_energy
    if min_energy is not None:
        kwargs['min_energy'] = min_energy
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
    if seed_catalog:
        if isinstance(seed_catalog, catalog.Catalog):
            kwargs['seed_catalog'] = seed_catalog.id
        else:
            kwargs['seed_catalog'] = seed_catalog
    if source_catalog:
        if isinstance(source_catalog, catalog.Catalog):
            kwargs['source_catalog'] = source_catalog.id
        else:
            kwargs['source_catalog'] = source_catalog
            
    result = util.callm("%s/%s" % ('playlist', 'static'), kwargs)
    return [Song(**util.fix(s_dict)) for s_dict in result['response']['songs']]
