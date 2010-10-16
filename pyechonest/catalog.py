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
import util
from proxies import CatalogProxy

# deal with datetime in json
dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

class Catalog(CatalogProxy):
    """
    A Catalog object
    
    Create an catalog object like so.
    >>> c = catalog.Catalog('CAXGEJB12AAA95CBF1')
    >>> c = catalog.Catalog('test1')
    
    Attributes: (**attributes** are guaranteed to exist as soon as a catalog object exists)
        **id** (str): Catalog ID
        
        **name** (str): Catalog Name
    """
    def __init__(self, id, type=None, **kwargs):
        """
        Create a catalog object
        
        if a catalog by that name for this API key does not exist, create a new one
        """
        super(Catalog, self).__init__(id, type, **kwargs)
    
    def __repr__(self):
        return "<%s - %s>" % (self._object_type.encode('utf-8'), self.name.encode('utf-8'))
    
    def __str__(self):
        return self.name.encode('utf-8')
    
    def update(self, items):
        """
        Update a catalog object
        
        items is a list of dicts describing update data and action codes (see api docs)
        """
        post_data = {}
        
        items_json = json.dumps(items, default=dthandler)
        post_data['data'] = items_json

        return self.post_attribute("update", data=post_data)
    
    def status(self, ticket):
        """
        Check the status of a catalog update
        """
        return self.get_attribute_simple("status", ticket=ticket)
    
    def profile(self):
        """
        Check the status of a catalog update
        """
        return self.get_attribute("profile")
    
    def read(self, buckets=None, results=15, start=0):
        """
        Returns all of the data in the catalog; also returns info requested via bucket
        """
        kwargs = {}
        kwargs['bucket'] = buckets or []
        response = self.get_attribute("read", results=results, start=start, **kwargs)
        return response['catalog']
    
    def delete(self):
        """
        Deletes the entire catalog
        """
        return self.post_attribute("delete")
    

def list(results=30, start=0):
    """
    Returns list of all catalogs created on this API key
    """
    result = util.callm("%s/%s" % ('catalog', 'list'), {'results':results, 'start':start})
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Catalog(**fix(d)) for d in result['response']['catalogs']]
    
