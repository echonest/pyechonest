#!/usr/bin/env python
# encoding: utf-8
"""
A Python interface to the The Echo Nest's web API.  See
http://developer.echonest.com/ for details.
"""

from pyechonest.decorators import memoized
from pyechonest import document
from pyechonest import util


class Artist(object):
    def __init__(self, identifier):
        if len(identifier)==18:
            identifier = 'music://id.echonest.com/~/AR/' + identifier
        self._identifier = identifier
        self._name = None
        self.audio = document.WebDocumentSet(identifier, 'get_audio')
        self.blogs = document.WebDocumentSet(identifier, 'get_blogs')
        self.news = document.WebDocumentSet(identifier, 'get_news')
        self.reviews = document.WebDocumentSet(identifier, 'get_reviews')
        self.similar = SimilarDocumentSet(identifier)
        self.video = document.WebDocumentSet(identifier, 'get_video')

    @property
    @memoized
    def familiarity(self):
        """Returns our numerical estimation of how 
        familiar an artist currently is to the world."""
        return float(util.call('get_familiarity', {'id': self.identifier}).findtext('artist/familiarity'))

    @property
    @memoized
    def hotttnesss(self):
        """Returns our numerical description of how 
        hottt an artist currently is."""
        return float(util.call('get_hotttnesss', {'id': self.identifier}).findtext('artist/hotttnesss'))

    @property
    @memoized
    def name(self):
        if self._name is None:
            self._name = util.call('get_profile', {'id': self.identifier}).findtext('artist/name')
        return self._name
        
    @property
    def identifier(self):
        """A unique identifier for an artist.
        See http://developer.echonest.com/docs/datatypes/
        for more information"""
        return self._identifier

    @property
    def thing_id(self):
        return self._identifier.split('/')[-1]
    
    @property
    @memoized
    def urls(self):
        """Get links to the artist's official site, MusicBrainz site, 
        MySpace site, Wikipedia article, Amazon list, and iTunes page."""
        response = util.call('get_urls', {'id': self.identifier}).find('artist').getchildren()
        return dict((url.tag[:-4], url.text) for url in response if url.tag[-4:] == '_url')

    @property
    @memoized
    def terms(self):
        response = util.call('get_top_terms', {'id': self.identifier}).findall('terms/term')
        return [e.text for e in response]


    def __repr__(self):
        return "<Artist '%s'>" % self.name
    
    def __str__(self):
        return self.name


TRUTH = {True: 'Y', False: 'N'}

@memoized
def search_artists(name, exact=False, sounds_like=True, rows=15):
    """Search for an artist using a query on the artist name.
    This may perform a sounds-like search to correct common 
    spelling mistakes."""
    params = {'query': name, 'exact': TRUTH[exact], 
                'sounds_like': TRUTH[sounds_like], 'rows': rows}
    response = util.call('search_artists', params).findall('artists/artist')
    return [Artist(a.findtext('id')) for a in response]


@memoized
def get_top_hottt_artists(rows=15):
    """Retrieves a list of the top hottt artists.
    Do not request this more than once an hour."""
    response = util.call('get_top_hottt_artists', {'rows': rows}).findall('artists/artist')
    return [Artist(a.findtext('id')) for a in response]


@memoized
def search_tracks(name, start=0, rows=15):
    """Search for audio using a query on the track, album, or artist name."""
    params = {'query': name, 'start': start, 'rows':rows}
    response = util.call('search_tracks', params).findall('results/doc')
    tracks = []
    for element in response:
        parsed = dict((e.tag, e.text) for e in element.getchildren())
        print parsed
        if element.attrib.has_key('id'):
            parsed.update({'id': element.attrib['id']})
        tracks.append(parsed)
    return tracks


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
        return Artist(element.findtext('id'))

