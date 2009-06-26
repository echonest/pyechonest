"""
A Python interface to the The Echo Nest's Analyze web API.  See
http://developer.echonest.com/ for details.  Audio analysis is returned
as XML objects.
"""

__version__ = "$Revision: 0 $"
# $Source$

# Standard library modules.
from functools import partial
import os
import sys
import urllib

# Modules in this package.
from endev import config
from endev import util



class Artist(object):
    
    # Any variable in this listing is fetched over the network once
    # and then cached.  Calling refreshCachedVariables will force a
    # refresh.
    CACHED_VARIABLES = ('audio',
                        'blogs',
                        'familiarity',
                        'hotttnesss',
                        'news',
                        'profile',
                        'reviews',
                        'similar',
                        'top_terms',
                        'urls',
                        'video')

    def __init__(self, identifier, name=None):
        # Check identifier. if it's an artistID, ok. otherwise,
        # treat is as a name and search...? whatev, look at Paul's javashell
        
        self.parsers = {    'audio':generalParser,
                            'blogs':generalParser,
                            'familiarity':artistParser,
                            'hotttnesss':artistParser,
                            'news':generalParser,
                            'profile':artistParser,
                            'reviews':generalParser,
                            'similar':similarParser,
                            'top_terms':generalParser,
                            'urls':artistParser,
                            'video':generalParser
                            }
        self.name = name
        self.id = identifier
        # Initialize cached variables to None.
        for cachedVar in Artist.CACHED_VARIABLES : 
            self.__setattr__(cachedVar, None)
            self.__setattr__('_' + cachedVar + '_query', None)
        
    def lalala__getattribute__(self, name):
        """
        This function has been modified to support caching of
        variables retrieved over the network. As a result, each 
        of the `CACHED_VARIABLES` is available as an accessor.
        """
        if name in Artist.CACHED_VARIABLES :
            if object.__getattribute__(self, name) is None :
                getter = partial(util.apiFunctionPrototype, 'get_' + name)
                _id = 'music://id.echonest.com/~/AR/' + object.__getattribute__(self, 'id')
                value = getter(_id)
                parseFunction = object.__getattribute__(self, 'parsers').get(name)
                if parseFunction :
                    value, query = parseFunction(value)
                self.__setattr__(name, value)
                self.__setattr__('_' + name + '_query', query)
        return object.__getattribute__(self, name)
        
    def __getattribute__(self, name):
        if name in Artist.CACHED_VARIABLES:
            if object.__getattribute__(self, name) is None :
                return self._get(name)
        return object.__getattribute__(self, name)

    def _get(self, name, start=None, rows=None):
        """
        This function has been modified to support caching of
        variables retrieved over the network. As a result, each 
        of the `CACHED_VARIABLES` is available as an accessor.
        """
        getter = partial(util.apiFunctionPrototype, 'get_' + name, start=start, rows=rows)
        _id = 'music://id.echonest.com/~/AR/' + object.__getattribute__(self, 'id')
        value = getter(_id)
        parseFunction = object.__getattribute__(self, 'parsers').get(name)
        if parseFunction :
            value, query = parseFunction(value)
        self.__setattr__(name, value)
        self.__setattr__('_' + name + '_query', query)
        return object.__getattribute__(self, name)

    def _query(self, name, start=0, rows=15):
        if start is None:
            start = 0
        if rows is None:
            rows = 15
        if name in Artist.CACHED_VARIABLES:
            if object.__getattribute__(self, name) is None:
                return self._get(name, start, rows)
            old_query = object.__getattribute__(self, '_' + name + '_query')
            if (int(old_query['rows']) == rows) and (int(old_query['start']) == start):
                return object.__getattribute__(self, name)
            return self._get(name, start, rows)
        else:
            raise TypeError('wtf')

    def get_audio(self, start=None, rows=None):
        return self._query('audio', start, rows)

    def get_blogs(self, start=None, rows=None):
        return self._query('blogs', start, rows)

    def get_familiarity(self):
        return self._query('familiarity')

    def get_hotttnesss(self):
        return self._query('blogs')

    def get_news(self, start=None, rows=None):
        return self._query('news', start, rows)

    def get_profile(self):
        return self._query('profile')

    def get_reviews(self, start=None, rows=None):
        return self._query('reviews', start, rows)

    def get_similar(self, start=None, rows=None):
        return self._query('similar', start, rows)

    def get_top_terms(self, start=None, rows=None):
        return self._query('top_terms', start, rows)

    def get_urls(self):
        return self._query('urls')

    def get_video(self, start=None, rows=None):
        return self._query('video', start, rows)

    def __repr__(self):
        return "<Artist '%s'>" % self.name
    
    def __str__(self):
        return self.name

    def refreshCachedVariables( self ) :
        """
        Forces all cached variables to be updated over the network.
        """
        for cachedVar in AudioAnalysis.CACHED_VARIABLES : 
            self.__setattr__(cachedVar, None)
            self.__getattribute__(cachedVar)


def generalParser(doc):
    query = {}
    for element in doc.firstChild.childNodes[1].childNodes:
        query[element.getAttribute('name')] = element.firstChild.data
    out = []
    for result in doc.firstChild.childNodes[3].childNodes:
        element = {}
        for node in result.childNodes:
            element[node.nodeName] = node.firstChild.data
        out.append(element)
    return out, query

def artistParser(doc):
    out = {}
    for node in doc.firstChild.childNodes[2].childNodes:
        out[node.nodeName] = node.firstChild.data
    return out, None

def similarParser(doc):
    query = {}
    for element in doc.firstChild.childNodes[1].childNodes:
        query[element.getAttribute('name')] = element.firstChild.data
    out = []
    for result in doc.firstChild.childNodes[2].childNodes:
        element = {}
        for node in result.childNodes:
            element[node.nodeName] = node.firstChild.data
        out.append(element)
    return out, query


def search_artists(name, exact=False, sounds_like=True, rows=15):
    if exact is True:
        exact = 'Y'
    else:
        exact = 'N'
    if sounds_like is True:
        sounds_like = 'Y'
    else:
        sounds_like = 'N'
    params = urllib.urlencode({'query': name, 'api_key': config.API_KEY, 'exact': exact, 'sounds_like':sounds_like, 'rows':rows})
    url = 'http://%s%s%s?%s&version=3' % (config.API_HOST, config.API_SELECTOR, 'search_artists', params)
    f = urllib.urlopen( url )
    doc = parseXMLString(f.read())
    artists = []
    for result in doc.firstChild.childNodes[2].childNodes:
        artist = {}
        for node in result.childNodes:
            artist[node.nodeName] = node.firstChild.data
        artists.append(artist)
    return artists
    
def get_similar(nameList, start=0, rows=15):
    pass

def parseXMLString( xmlString ) :
    """
    This function is meant to modularize the handling of XML strings
    returned by the web API.  Overriding this method will change how
    the entire package parses XML strings.

    :param xmlString: The plaintext string of XML to parse.

    :return: An object representation of the XML string, in this case a
        xml.dom.minidom representation.
    """
    doc = xml.dom.minidom.parseString(xmlString)
    status_code = int(doc.getElementsByTagName('code')[0].firstChild.data)
    if status_code not in SUCCESS_STATUS_CODES :
        status_message = doc.getElementsByTagName('message')[0].firstChild.data
        if status_code in FAILURE_API_KEY_STATUS_CODES:
            raise EchoNestAPIKeyError(status_code, status_message)
        elif status_code in FAILURE_THING_ID_STATUS_CODES:
            raise EchoNestAPIThingIDError(status_code, status_message)
        else:
            raise EchoNestAPIError(status_code, status_message)
    return doc
