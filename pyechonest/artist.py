#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2010-04-25.

The Artist module loosely covers http://beta.developer.echonest.com/artist.html
Refer to the official api documentation if you are unsure about something.
"""

import util
from proxies import ArtistProxy
from results import Result

class Artist(ArtistProxy):
    """
    An Artist object
    
    Create an artist object like so:
        a = artist.Artist('ARH6W4X1187B99274F')
        a = artist.Artist('the national')
        a = artist.Artist('musicbrainz:artist:a74b1b7f-71a5-4011-9441-d0b5e4122711')
    
    Attributes: (**attributes** are guaranteed to exist as soon as an artist object exists)
        **id**: Echo Nest Artist ID
        **name**: Artist Name
        hotttnesss: A float representing an artist's hotttnesss
        audio: A list of audio document Result objects
        biographies: A list of biography document Result objects
        blogs: A list of blog document Result objects
        familiarity: A float representing an artist's familiarity 
        images: A list of image document Result objects
        news: A list of news document Result objects
        reviews: A list of review document Result objects
        similar: A list of similar Artist objects
        terms: A list of terms document Result objects
        urls: A urls result object
        video: A list of video document Result objects
    """
    def __init__(self, id, **kwargs):
        super(Artist, self).__init__(id, **kwargs)
    
    def __repr__(self):
        return "<%s - %s>" % (self.type.encode('utf-8'), self.name.encode('utf-8'))
    
    def __str__(self):
        return self.name.encode('utf-8')
     
    def get_hotttnesss(self, cache=True):
        """Get our numerical description of how hottt an artist currently is
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing hotttnesss.
        """
        if not (cache and ('hotttnesss' in self.cache)):
            response = self.get_attribute('hotttnesss')
            self.cache['hotttnesss'] = response['artist']['hotttnesss']
        return self.cache['hotttnesss']
    
    hotttnesss = property(get_hotttnesss)
    
    def get_audio(self, results=15, start=0, cache=True):
        """Get a list of audio documents found on the web related to an artist
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            results: An integer number of results to return
            start: An integer starting value for the result set
        
        Returns:
            A list of audio document Result objects
        """
        
        if cache and ('audio' in self.cache) and results==15 and start==0:
            return [Result('audio', a) for a in self.cache['audio']]
        else:
            response = self.get_attribute('audio', results=results, start=start)
            if results==15 and start==0:
                self.cache['audio'] = response['audio']
            return [Result('audio', a) for a in response['audio']]

    
    audio = property(get_audio)
    
    def get_biographies(self, results=15, start=0, license='unknown', cache=True):
        """Get a list of artist biographies
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            results: An integer number of results to return
            start: An integer starting value for the result set
            license: A string specifying the desired license type
        
        Returns:
            A list of biography document Result objects
        """
        if cache and ('biographies' in self.cache) and results==15 and start==0 and license=='unknown':
            return [Result('biographies', a) for a in self.cache['biographies']]
        else:
            response = self.get_attribute('biographies', results=results, start=start)
            if results==15 and start==0 and license=='unknown':
                self.cache['biographies'] = response['biographies']
            return [Result('biographies', a) for a in response['biographies']]
    
    biographies = property(get_biographies)    
    
    def get_blogs(self, results=15, start=0, cache=True):
        """Get a list of blog articles related to an artist
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            results: An integer number of results to return
            start: An ingteger starting value for the result set
        
        Returns:
            A list of blog document Result objects
        """
        if cache and ('blogs' in self.cache) and results==15 and start==0:
            return [Result('blogs', a) for a in self.cache['blogs']]
        else:
            response = self.get_attribute('blogs', results=results, start=start)
            if results==15 and start==0:
                self.cache['blogs'] = response['blogs']
            return [Result('blogs', a) for a in response['blogs']]
    
    blogs = property(get_blogs)
       
    def get_familiarity(self, cache=True):
        """Get our numerical estimation of how familiar an artist currently is to the world
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing familiarity.
        """
        if not (cache and ('familiarity' in self.cache)):
            response = self.get_attribute('familiarity')
            self.cache['familiarity'] = response['artist']['familiarity']
        return self.cache['familiarity']
    
    familiarity = property(get_familiarity)    
    
    def get_images(self, results=15, start=0, license='unknown', cache=True):
        """Get a list of artist images
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            results: An integer number of results to return
            start: An integer starting value for the result set
            license: A string specifying the desired license type
        
        Returns:
            A list of image document Result objects
        """
        if cache and ('images' in self.cache) and results==15 and start==0 and license=='unknown':
            return [Result('images', a) for a in self.cache['images']]
        else:
            response = self.get_attribute('images', results=results, start=start)
            if results==15 and start==0 and license=='unknown':
                self.cache['images'] = response['images']
            return [Result('images', a) for a in response['images']]
    
    images = property(get_images)    
    
    def get_news(self, results=15, start=0, cache=True):
        """Get a list of news articles found on the web related to an artist
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            results: An integer number of results to return
            start: An integer starting value for the result set
        
        Returns:
            A list of news document Result objects
        """
        if cache and ('news' in self.cache) and results==15 and start==0:
            return [Result('news', a) for a in self.cache['news']]
        else:
            response = self.get_attribute('news', results=results, start=start)
            if results==15 and start==0:
                self.cache['news'] = response['news']
            return [Result('news', a) for a in response['news']]

    
    news = property(get_news)
    
    def get_reviews(self, results=15, start=0, cache=True):
        """Get reviews related to an artist's work
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            results: An integer number of results to return
            start: An integer starting value for the result set
        
        Returns:
            A list of review document Result objects
        """
        if cache and ('reviews' in self.cache) and results==15 and start==0:
            return [Result('reviews', a) for a in self.cache['reviews']]
        else:
            response = self.get_attribute('reviews', results=results, start=start)
            if results==15 and start==0:
                self.cache['reviews'] = response['reviews']
            return [Result('reviews', a) for a in response['reviews']]

    
    reviews = property(get_reviews)
    
    def get_similar(self, results=15, start=0, cache=True, max_familiarity=None, min_familiarity=None, \
                    max_hotttnesss=None, min_hotttnesss=None):
        """Return similar artists to this one
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            results: An integer number of results to return
            start: An integer starting value for the result set
            max_familiarity: A float specifying the max familiarity of artists to search for
            min_familiarity: A float specifying the min familiarity of artists to search for
            max_hotttnesss: A float specifying the max hotttnesss of artists to search for
            min_hotttnesss: A float specifying the max hotttnesss of artists to search for
        Returns:
            A list of similar Artist objects
        """
        kwargs = {}
        if max_familiarity:
            kwargs['max_familiarity'] = max_familiarity
        if min_familiarity:
            kwargs['min_familiarity'] = min_familiarity
        if max_hotttnesss:
            kwargs['max_hotttnesss'] = max_hotttnesss
        if min_hotttnesss:
            kwargs['min_hotttnesss'] = min_hotttnesss

        # we need this to fix up all the dict keys to be strings, not unicode objects    
        fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
        
        if cache and ('similar' in self.cache) and results==15 and start==0 and (not kwargs):
            return [Artist(**fix(a)) for a in self.cache['similar']]
        else:
            response = self.get_attribute('similar', results=results, start=start, **kwargs)
            if results==15 and start==0 and (not kwargs):
                self.cache['similar'] = response['artists']
            return [Artist(**fix(a)) for a in response['artists']]
        
    
    similar = property(get_similar)    
    
    def get_terms(self, sort='weight', cache=True):
        """Get the terms associated with an artist
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            sort: A string specifying the desired sorting type (weight or frequency)
            
        Results:
            A list of term document Result objects
        """
        if cache and ('terms' in self.cache) and sort=='weight':
            return [Result('terms', a) for a in self.cache['terms']]
        else:
            response = self.get_attribute('terms', sort=sort)
            if sort=='weight':
                self.cache['terms'] = response['terms']
            return [Result('terms', a) for a in response['terms']]
    
    terms = property(get_terms)
    
    def get_urls(self, cache=True):
        """Get the urls for an artist
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
        Results:
            A url document Result objects
        """
        if not (cache and ('urls' in self.cache)):
            response = self.get_attribute('urls')
            self.cache['urls'] = response['urls']
        return Result('urls', self.cache['urls'])
    
    urls = property(get_urls)    
    
    def get_video(self, results=15, start=0, cache=True):
        """Get a list of video documents found on the web related to an artist
        
        Args:
            cache: A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            results: An integer number of results to return
            start: An integer starting value for the result set
        
        Returns:
            A list of video document Result objects
        """
        if cache and ('video' in self.cache) and results==15 and start==0:
            return [Result('video', a) for a in self.cache['video']]
        else:
            response = self.get_attribute('video', results=results, start=start)
            if results==15 and start==0:
                self.cache['video'] = response['video']
            return [Result('video', a) for a in response['video']]
    
    video = property(get_video)

    def get_foreign_id(self, idspace='musicbrainz', cache=True):
        """Get the foreign id for this artist for a specific id space
        
        Args:
            idspace: A string indicating the idspace to fetch a foreign id for.
        
        Returns:
            A foreign ID string
        """
        if not (cache and ('foreign_ids' in self.cache) and filter(lambda d: d.get('catalog') == idspace, self.cache['foreign_ids'])):
            response = self.get_attribute('profile', bucket=['id:'+idspace])
            foreign_ids = response['artist'].get("foreign_ids")
            self.cache['foreign_ids'] = self.cache.get('foreign_ids', []) + foreign_ids
        cval = filter(lambda d: d.get('catalog') == idspace, self.cache.get('foreign_ids'))
        return cval[0].get('foreign_id') if cval else None
    

def search(name=None, description=None, results=15, buckets = None, limit=False, \
            fuzzy_match=False, sort=None, max_familiarity=None, min_familiarity=None, \
            max_hotttnesss=None, min_hotttnesss=None):
    """Search for artists by name, description, or constraint.
    
    Args:
        name: the name of an artist
        description: A string describing the artist
        results: An integer number of results to return
        buckets: A list of strings specifying which buck
        limit: A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
        fuzzy_match: A boolean indicating whether or not to search for similar sounding matches (only works with name)
        max_familiarity: A float specifying the max familiarity of artists to search for
        min_familiarity: A float specifying the min familiarity of artists to search for
        max_hotttnesss: A float specifying the max hotttnesss of artists to search for
        min_hotttnesss: A float specifying the max hotttnesss of artists to search for
    
    Returns:
        A list of Artist objects
    """
    buckets = buckets or []
    kwargs = {}
    if name:
        kwargs['name'] = name
    if description:
        kwargs['description'] = description
    if results:
        kwargs['results'] = results
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    if fuzzy_match:
        kwargs['fuzzy_match'] = 'true'
    if max_familiarity:
        kwargs['max_familiarity'] = max_familiarity
    if min_familiarity:
        kwargs['min_familiarity'] = min_familiarity
    if max_hotttnesss:
        kwargs['max_hotttnesss'] = max_hotttnesss
    if min_hotttnesss:
        kwargs['min_hotttnesss'] = min_hotttnesss
    if sort:
        kwargs['sort'] = sort
    
    """Search for artists"""
    result = util.callm("%s/%s" % ('artist', 'search'), kwargs)
    # we need this to fix up all the dict keys to be strings, not unicode objects
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Artist(**fix(a_dict)) for a_dict in result['response']['artists']]

def top_hottt(start=0, results=15, buckets = None, limit=False):
    """Get the top hotttest artists, according to The Echo Nest
    
    Args:
        results: An integer number of results to return
        start: An integer starting value for the result set
        buckets: A list of strings specifying which buck
        limit: A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
        
    Returns:
        A list of hottt Artist objects
        """
    buckets = buckets or []
    kwargs = {}
    if start:
        kwargs['start'] = start
    if results:
        kwargs['results'] = results
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    
    """Get top hottt artists"""
    result = util.callm("%s/%s" % ('artist', 'top_hottt'), kwargs)
    # we need this to fix up all the dict keys to be strings, not unicode objects
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Artist(**fix(a_dict)) for a_dict in result['response']['artists']]    


def top_terms(results=15):
    """Get a list of the top overall terms
        
    Args:
        results: An integer number of results to return
        
    Returns:
        A list of term document Result objects
    """
    
    kwargs = {}
    if results:
        kwargs['results'] = results
    
    """Get top terms"""
    result = util.callm("%s/%s" % ('artist', 'top_terms'), kwargs)
    return [Result('term', a_dict) for a_dict in result['response']['terms']]


def similar(names=None, ids=None, start=0, results=15, buckets = None, limit=False, max_familiarity=None, min_familiarity=None,
            max_hotttnesss=None, min_hotttnesss=None):
    """Return similar artists to this one
    
    Args:
        id: An artist id or list of ids
        name: An artist name or list of names
        results: An integer number of results to return
        start: An integer starting value for the result set
        buckets: A list of strings specifying which buck
        limit: A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
        max_familiarity: A float specifying the max familiarity of artists to search for
        min_familiarity: A float specifying the min familiarity of artists to search for
        max_hotttnesss: A float specifying the max hotttnesss of artists to search for
        min_hotttnesss: A float specifying the max hotttnesss of artists to search for
    Returns:
        A list of similar Artist objects
    """
    
    buckets = buckets or []
    kwargs = {}

    if ids:
        if not isinstance(ids, list):
            ids = [ids]
        kwargs['id'] = ids
    if names:
        if not isinstance(names, list):
            names = [names]
        kwargs['name'] = names
    if max_familiarity:
        kwargs['max_familiarity'] = max_familiarity
    if min_familiarity:
        kwargs['min_familiarity'] = min_familiarity
    if max_hotttnesss:
        kwargs['max_hotttnesss'] = max_hotttnesss
    if min_hotttnesss:
        kwargs['min_hotttnesss'] = min_hotttnesss
    if start:
        kwargs['start'] = start
    if results:
        kwargs['results'] = results
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'

    result = util.callm("%s/%s" % ('artist', 'similar'), kwargs)
    # we need this to fix up all the dict keys to be strings, not unicode objects
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Artist(**fix(a_dict)) for a_dict in result['response']['artists']]    

