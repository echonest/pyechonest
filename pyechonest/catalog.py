#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Scotty Vercoe on 2010-08-25.

The Catalog module loosely covers http://developer.echonest.com/docs/v4/catalog.html
Refer to the official api documentation if you are unsure about something.
"""
try:
    import json
except ImportError:
    import simplejson as json
import datetime

import warnings
import util
from proxies import CatalogProxy, ResultList
import artist, song

# deal with datetime in json
dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

def create_catalog_by_name(name, T="general"):
    """
    Creates a catalog object, with a given name. Does not check to see if the catalog already exists.

    Create a catalog object like
    """
    result = util.callm("catalog/create", {}, POST=True, 
                            data={"name":name, "type":T})
    result = result['response']
    return Catalog(result['id'], **dict( (k,result[k]) for k in ('name', 'type')))

class Catalog(CatalogProxy):
    """
    A Catalog object

    Attributes:
        id (str): Catalog ID

        name (str): Catalog Name

        read (list): A list of catalog items (objects if they are resolved, else dictionaries)

        feed (list): A list of dictionaries for news, blogs, reviews, audio, video for a catalog's artists

    Create an catalog object like so:

    >>> c = catalog.Catalog('CAGPXKK12BB06F9DE9') # get existing catalog
    >>> c = catalog.Catalog('test_song_catalog', 'song') # get existing or create new catalog

    """
    def __init__(self, id, type=None, **kwargs):
        """
        Create a catalog object (get a catalog by ID or get or create one given by name and type)

        Args:
            id (str): A catalog id or name

        Kwargs:
            type (str): 'song' or 'artist', specifying the catalog type

        Returns:
            A catalog object

        Example:

        >>> c = catalog.Catalog('my_songs', type='song')
        >>> c.id
        u'CAVKUPC12BCA792120'
        >>> c.name
        u'my_songs'
        >>>

        """
        super(Catalog, self).__init__(id, type, **kwargs)

    def __repr__(self):
        return "<%s - %s>" % (self._object_type.encode('utf-8'), self.name.encode('utf-8'))

    def __str__(self):
        return self.name.encode('utf-8')

    def update(self, items):
        """
        Update a catalog object

        Args:
            items (list): A list of dicts describing update data and action codes (see api docs)

        Kwargs:

        Returns:
            A ticket id

        Example:

        >>> c = catalog.Catalog('my_songs', type='song')
        >>> items
        [{'action': 'update',
          'item': {'artist_name': 'dAn ThE aUtOmAtOr',
                   'disc_number': 1,
                   'genre': 'Instrumental',
                   'item_id': '38937DDF04BC7FC4',
                   'play_count': 5,
                   'release': 'Bombay the Hard Way: Guns, Cars & Sitars',
                   'song_name': 'Inspector Jay From Dehli',
                   'track_number': 9,
                   'url': 'file://localhost/Users/tylerw/Music/iTunes/iTunes%20Media/Music/Dan%20the%20Automator/Bombay%20the%20Hard%20Way_%20Guns,%20Cars%20&%20Sitars/09%20Inspector%20Jay%20From%20Dehli.m4a'}}]
        >>> ticket = c.update(items)
        >>> ticket
        u'7dcad583f2a38e6689d48a792b2e4c96'
        >>> c.status(ticket)
        {u'ticket_status': u'complete', u'update_info': []}
        >>>

        """
        post_data = {}
        items_json = json.dumps(items, default=dthandler)
        post_data['data'] = items_json

        response = self.post_attribute("update", data=post_data)

        return response['ticket']

    def status(self, ticket):
        """
        Check the status of a catalog update

        Args:
            ticket (str): A string representing a ticket ID

        Kwargs:

        Returns:
            A dictionary representing ticket status

        Example:

        >>> ticket
        u'7dcad583f2a38e6689d48a792b2e4c96'
        >>> c.status(ticket)
        {u'ticket_status': u'complete', u'update_info': []}
        >>>

        """
        return self.get_attribute_simple("status", ticket=ticket)

    def get_profile(self):
        """
        Check the status of a catalog update

        Args:

        Kwargs:

        Returns:
            A dictionary representing ticket status

        Example:

        >>> c
        <catalog - test_song_catalog>
        >>> c.profile()
        {u'id': u'CAGPXKK12BB06F9DE9',
         u'name': u'test_song_catalog',
         u'pending_tickets': [],
         u'resolved': 2,
         u'total': 4,
         u'type': u'song'}
        >>>

        """
        result = self.get_attribute("profile")
        return result['catalog']

    profile = property(get_profile)
    def read_items(self, buckets=None, results=15, start=0,item_ids=None):
        """
        Returns data from the catalog; also expanded for the requested buckets.
        This method is provided for backwards-compatibility

        Args:

        Kwargs:
            buckets (list): A list of strings specifying which buckets to retrieve

            results (int): An integer number of results to return

            start (int): An integer starting value for the result set

        Returns:
            A list of objects in the catalog; list contains additional attributes 'start' and 'total'

        Example:

        >>> c
        <catalog - my_songs>
        >>> c.read_items(results=1)
        [<song - Harmonice Mundi II>]
        >>>
        """
        warnings.warn("catalog.read_items() is depreciated. Please use catalog.get_item_dicts() instead.")
        kwargs = {}
        kwargs['bucket'] = buckets or []
        kwargs['item_id'] = item_ids or []
        response = self.get_attribute("read", results=results, start=start, **kwargs)
        rval = ResultList([])
        if item_ids:
            rval.start=0;
            rval.total=len(response['catalog']['items'])
        else:
            rval.start = response['catalog']['start']
            rval.total = response['catalog']['total']
        for item in response['catalog']['items']:
            new_item = None
            # song items
            if 'song_id' in item:
                item['id'] = item.pop('song_id')
                item['title'] = item.pop('song_name')
                request = item['request']
                new_item = song.Song(**util.fix(item))
                new_item.request = request
            # artist item
            elif 'artist_id' in item:
                item['id'] = item.pop('artist_id')
                item['name'] = item.pop('artist_name')
                request = item['request']
                new_item = artist.Artist(**util.fix(item))
                new_item.request = request
            # unresolved item
            else:
                new_item = item
            rval.append(new_item)
        return rval

    read = property(read_items)

    def get_item_dicts(self, buckets=None, results=15, start=0,item_ids=None):
        """
        Returns data from the catalog; also expanded for the requested buckets

        Args:

        Kwargs:
            buckets (list): A list of strings specifying which buckets to retrieve

            results (int): An integer number of results to return

            start (int): An integer starting value for the result set

        Returns:
            A list of dicts representing objects in the catalog; list has additional attributes 'start' and 'total'

        Example:

        >>> c
        <catalog - my_songs>
        >>> c.read_items(results=1)
        [
                {
                    "artist_id": "AR78KRI1187B98E6F2",
                    "artist_name": "Art of Noise",
                    "date_added": "2012-04-02T16:50:02",
                    "foreign_id": "CAHLYLR13674D1CF83:song:1000",
                    "request": {
                        "artist_name": "The Art Of Noise",
                        "item_id": "1000",
                        "song_name": "Love"
                    },
                    "song_id": "SOSBCTO1311AFE7AE0",
                    "song_name": "Love"
                }
        ]
        """
        kwargs = {}
        kwargs['bucket'] = buckets or []
        kwargs['item_id'] = item_ids or []
        response = self.get_attribute("read", results=results, start=start, **kwargs)
        rval = ResultList(response['catalog']['items'])
        if item_ids:
            rval.start=0;
            rval.total=len(response['catalog']['items'])
        else:
            rval.start = response['catalog']['start']
            rval.total = response['catalog']['total']
        return rval

    item_dicts = property(get_item_dicts)

    def get_feed(self, buckets=None, since=None, results=15, start=0):
        """
        Returns feed (news, blogs, reviews, audio, video) for the catalog artists; response depends on requested buckets

        Args:

        Kwargs:
            buckets (list): A list of strings specifying which feed items to retrieve

            results (int): An integer number of results to return

            start (int): An integer starting value for the result set

        Returns:
            A list of news, blogs, reviews, audio or video document dicts;

        Example:

        >>> c
        <catalog - my_artists>
        >>> c.get_feed(results=15)
	{u'date_found': u'2011-02-06T07:50:25',
	 u'date_posted': u'2011-02-06T07:50:23',
 	 u'id': u'caec686c0dff361e4c53dceb58fb9d2f',
 	 u'name': u'Linkin Park \u2013 \u201cWaiting For The End\u201d + \u201cWhen They Come For Me\u201d 2/5 SNL',
 	 u'references': [{u'artist_id': u'ARQUMH41187B9AF699',
        	          u'artist_name': u'Linkin Park'}],
	 u'summary': u'<span>Linkin</span> <span>Park</span> performed "Waiting For The End" and "When They Come For Me" on Saturday Night Live. Watch the videos below and pick up their album A Thousand Suns on iTunes, Amazon MP3, CD    Social Bookmarking ... ',
	 u'type': u'blogs',
	 u'url': u'http://theaudioperv.com/2011/02/06/linkin-park-waiting-for-the-end-when-they-come-for-me-25-snl/'}
        >>>
        """
        kwargs = {}
        kwargs['bucket'] = buckets or []
	if since:
		kwargs['since']=since
        response = self.get_attribute("feed", results=results, start=start, **kwargs)
        rval = ResultList(response['feed'])
        return rval

    feed = property(get_feed)


    def delete(self):
        """
        Deletes the entire catalog

        Args:

        Kwargs:

        Returns:
            The deleted catalog's id.

        Example:

        >>> c
        <catalog - test_song_catalog>
        >>> c.delete()
        {u'id': u'CAXGUPY12BB087A21D'}
        >>>

        """
        return self.post_attribute("delete")

    def play(self, items, plays=None):
        return self.get_attribute("play", item=items, plays=plays)

    def skip(self, items, skips=None):
        return self.get_attribute("skip", item=items, skips=skips)

    def keyvalues(self):
        return self.get_attribute("keyvalues")['keyvalues']

    def favorite(self, items, favorite=None):
        if favorite != None:
            favorite = str(favorite).lower()
        return self.get_attribute("favorite", item=items, favorite=favorite)

    def ban(self, items, ban=None):
        if ban != None:
            ban = str(ban).lower()
        return self.get_attribute("ban", item=items, ban=ban)

    def rate(self, items, rating=None):
        return self.get_attribute("rate", item=items, rating=rating)
        
def get_catalog_by_name(name):
    """
    Grabs a catalog by name, if its there on the api key.
    Otherwise, an error is thrown (mirroring the API)
    """
    kwargs = {
            'name' : name,
        }
    result = util.callm("%s/%s" % ('catalog', 'profile'), kwargs)
    return Catalog(**util.fix(result['response']['catalog']))

def list_catalogs(results=30, start=0):
    """
    Returns list of all catalogs created on this API key

    Args:

    Kwargs:
        results (int): An integer number of results to return

        start (int): An integer starting value for the result set

    Returns:
        A list of catalog objects

    Example:

    >>> catalog.list_catalogs()
    [<catalog - test_artist_catalog>, <catalog - test_song_catalog>, <catalog - my_songs>]
    >>>

    """
    result = util.callm("%s/%s" % ('catalog', 'list'), {'results': results, 'start': start})
    cats = [Catalog(**util.fix(d)) for d in result['response']['catalogs']]
    start = result['response']['start']
    total = result['response']['total']
    return ResultList(cats, start, total)

