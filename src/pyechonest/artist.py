#!/usr/bin/env python
# encoding: utf-8
"""
A Python interface to the The Echo Nest's web API.  See
http://developer.echonest.com/ for details.
"""

from pyechonest.config import CACHE
from pyechonest import document
import pyechonest.util as util


class Artist(object):
    def __init__(self, identifier, name=None):
        if len(identifier)==18:
            identifier = 'music://id.echonest.com/~/AR/' + identifier
        self._identifier = identifier
        self._name = name
        self._audio = document.WebDocumentSet(identifier, 'get_audio')
        self._blogs = document.WebDocumentSet(identifier, 'get_blogs')
        self._news = document.WebDocumentSet(identifier, 'get_news')
        self._reviews = document.WebDocumentSet(identifier, 'get_reviews')
        self._similar = SimilarDocumentSet(identifier)
        self._video = document.WebDocumentSet(identifier, 'get_video')
        self._familiarity = None
        self._hotttnesss = None
        self._urls = None
        self._terms = None

    def audio(self, rows=15, start=0, refresh=False):
        if refresh or not CACHE:
            self._audio = document.WebDocumentSet(self._identifier, 'get_audio')
        return self._audio[start:start + rows]

    def blogs(self, rows=15, start=0, refresh=False):
        if refresh or not CACHE:
            self._blogs = document.WebDocumentSet(self._identifier, 'get_blogs')
        return self._blogs[start:start + rows]
        
    def news(self, rows=15, start=0, refresh=False):
        if refresh or not CACHE:
            self._news = document.WebDocumentSet(self._identifier, 'get_news')
        return self._news[start:start + rows]
    
    def reviews(self, rows=15, start=0, refresh=False):
        if refresh or not CACHE:
            self._reviews = document.WebDocumentSet(self._identifier, 'get_reviews')
        return self._reviews[start:start + rows]
    
    def similar(self, rows=15, start=0, refresh=False):
        if refresh or not CACHE:
            self._similar = SimilarDocumentSet(self._identifier)
        return self._similar[start:start + rows]
    
    def video(self, rows=15, start=0, refresh=False):
        if refresh or not CACHE:
            self._video = document.WebDocumentSet(self._identifier, 'get_video')
        return self._video[start:start + rows]

    def familiarity(self, refresh=True):
        """Returns our numerical estimation of how 
        familiar an artist currently is to the world."""
        if self._familiarity is None or not CACHE:
            try:
                params = {'id': self.identifier}
                response = util.call('get_familiarity', params).findtext('artist/familiarity')
                self._familiarity = float(response)
            except:
                self.familiarity = 0
        return self._familiarity

    def hotttnesss(self, refresh=True):
        """Returns our numerical description of how 
        hottt an artist currently is."""
        if self._hotttnesss is None or not CACHE:
            try:
                params = {'id': self.identifier}
                response = util.call('get_hotttnesss', params).findtext('artist/hotttnesss')
                self._hotttnesss = float(response)
            except:
                self._hotttnesss = 0
        return self._hotttnesss

    @property
    def name(self):
        if self._name is None or not CACHE:
            self._name = util.call('get_profile', {'id': self.identifier}).findtext('artist/name')
        return self._name
        
    @property
    def identifier(self):
        """A unique identifier for an artist.
        See http://developer.echonest.com/docs/datatypes/
        for more information"""
        return self._identifier
    
    @property
    def urls(self):
        """Get links to the artist's official site, MusicBrainz site, 
        MySpace site, Wikipedia article, Amazon list, and iTunes page."""
        if self._urls is None or not CACHE:
            response = util.call('get_urls', {'id': self.identifier}).find('artist').getchildren()
            self._urls =  dict((url.tag[:-4], url.text) for url in response if url.tag[-4:] == '_url')
        return self._urls

    def terms(self):
        if self._terms is None or not CACHE:
            response = util.call('get_top_terms', {'id': self.identifier}).findall('terms/term')
            self._terms = [e.text for e in response]
        return self._terms


    def __repr__(self):
        return "<Artist '%s'>" % self.name
    
    def __str__(self):
        return self.name
        
    def clear_cache(self):
        pass


TRUTH = {True: 'Y', False: 'N'}

SEARCH_ARTISTS_CACHE = {}

def search_artists(name, exact=False, sounds_like=True, rows=15, refresh=False):
    """Search for an artist using a query on the artist name.
    This may perform a sounds-like search to correct common 
    spelling mistakes."""
    global SEARCH_ARTISTS_CACHE
    if CACHE and not refresh:
        try:
            return SEARCH_ARTISTS_CACHE[(name, exact, sounds_like, rows)]
        except KeyError:
            pass
    params = {'query': name, 'exact': TRUTH[exact], 
                'sounds_like': TRUTH[sounds_like], 'rows': rows}
    response = util.call('search_artists', params).findall('artists/artist')
    value = [Artist(a.findtext('id'), a.findtext('name')) for a in response]
    SEARCH_ARTISTS_CACHE[(name, exact, sounds_like, rows)] = value
    return value


TOP_HOTTT_ARTISTS_CACHE = []
def get_top_hottt_artists(rows=15, refresh=False):
    """Retrieves a list of the top hottt artists.
    Do not request this more than once an hour."""
    global TOP_HOTTT_ARTISTS_CACHE
    if TOP_HOTTT_ARTISTS_CACHE==[] or refresh or not CACHE:
        response = util.call('get_top_hottt_artists', {'rows': rows}).findall('artists/artist')
        TOP_HOTTT_ARTISTS_CACHE = [Artist(a.findtext('id'), a.findtext('name')) for a in response]
    return TOP_HOTTT_ARTISTS_CACHE


class SimilarDocumentSet(document.DocumentSet):
    def __init__(self, identifier):
        super(SimilarDocumentSet, self).__init__(identifier, 'get_similar', 'similar/artist')

    def __len__(self):
        if self._len is None:
            self._len = 15
        return self._len

    def __getitem__(self, k):
        if isinstance(k, (int, long)):
            if k > 15:
                raise util.EchoNestAPIError(5, 'Invalid parameter: "rows" must be less than or equal to 15')
            return self._parse_element(self._cache[0].findall(self.element_path)[k])
        elif not isinstance(k, slice):
            raise TypeError
        if k.stop > 15:
            raise util.EchoNestAPIError(5, 'Invalid parameter: "rows" must be less than or equal to 15')
        start = k.start or 0
        stop = k.stop or len(self)
        items = []
        elements = self._cache[0].findall(self.element_path)[start:stop]
        items.extend([self._parse_element(e) for e in elements])
        return items

    def _parse_element(self, element):
        return Artist(element.findtext('id'), element.findtext('name'));

