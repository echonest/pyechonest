#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2010-04-25.
"""
import util

class ResultList(list):
    def __init__(self, li, start=0, total=0):
        self.extend(li)
        self.start = start
        if total == 0:
            total = len(li)
        self.total = total

class GenericProxy(object):
    def __init__(self):
        self.cache = {}
    
    def get_attribute(self, method_name, **kwargs):
        result = util.callm("%s/%s" % (self._object_type, method_name), kwargs)
        return result['response']
    
    def post_attribute(self, method_name, **kwargs):
        data = kwargs.pop('data') if 'data' in kwargs else {}
        result = util.callm("%s/%s" % (self._object_type, method_name), kwargs, POST=True, data=data)
        return result['response']
    

class ArtistProxy(GenericProxy):
    def __init__(self, identifier, buckets = None, **kwargs):
        super(ArtistProxy, self).__init__()
        buckets = buckets or []
        self.id = identifier
        self._object_type = 'artist'
        kwargs = dict((str(k), v) for (k,v) in kwargs.iteritems())
        # the following are integral to all artist objects... the rest is up to you!
        core_attrs = ['name']
        
        if not all(ca in kwargs for ca in core_attrs):
            profile = self.get_attribute('profile', **{'bucket':buckets})
            kwargs.update(profile.get('artist'))
        [self.__dict__.update({ca:kwargs.pop(ca)}) for ca in core_attrs+['id'] if ca in kwargs]        
        self.cache.update(kwargs)
    
    def get_attribute(self, *args, **kwargs):
        if util.short_regex.match(self.id) or util.long_regex.match(self.id) or util.foreign_regex.match(self.id):
            kwargs['id'] = self.id
        else:
            kwargs['name'] = self.id
        return super(ArtistProxy, self).get_attribute(*args, **kwargs)
    

class CatalogProxy(GenericProxy):
    def __init__(self, identifier, type, buckets = None, **kwargs):
        super(CatalogProxy, self).__init__()
        buckets = buckets or []
        self.id = identifier
        self._object_type = 'catalog'
        kwargs = dict((str(k), v) for (k,v) in kwargs.iteritems())
        # the following are integral to all catalog objects... the rest is up to you!
        core_attrs = ['name']
        if not all(ca in kwargs for ca in core_attrs):
            if util.short_regex.match(self.id) or util.long_regex.match(self.id) or util.foreign_regex.match(self.id):
                profile = self.get_attribute('profile')
                kwargs.update(profile['catalog'])
            else:
                if not type:
                    raise Exception('You must specify a "type"!')
                try:
                    profile = self.get_attribute('profile')
                    existing_type = profile['catalog'].get('type', 'Unknown')
                    if type != existing_type:
                        raise Exception("Catalog type requested (%s) does not match existing catalog type (%s)" % (type, existing_type))
                    
                    kwargs.update(profile['catalog'])
                except util.EchoNestAPIError:
                    profile = self.post_attribute('create', type=type, **kwargs)
                    kwargs.update(profile)
        [self.__dict__.update({ca:kwargs.pop(ca)}) for ca in core_attrs+['id'] if ca in kwargs]
        self.cache.update(kwargs)
    
    def get_attribute_simple(self, *args, **kwargs):
        # omit name/id kwargs for this call
        return super(CatalogProxy, self).get_attribute(*args, **kwargs)
    
    def get_attribute(self, *args, **kwargs):
        if util.short_regex.match(self.id) or util.long_regex.match(self.id) or util.foreign_regex.match(self.id):
            kwargs['id'] = self.id
        else:
            kwargs['name'] = self.id
        return super(CatalogProxy, self).get_attribute(*args, **kwargs)
    
    def post_attribute(self, *args, **kwargs):
        if util.short_regex.match(self.id) or util.long_regex.match(self.id) or util.foreign_regex.match(self.id):
            kwargs['id'] = self.id
        else:
            kwargs['name'] = self.id
        return super(CatalogProxy, self).post_attribute(*args, **kwargs)
    

class PlaylistProxy(GenericProxy):
    def __init__(self, session_id = None, buckets = None, **kwargs):
        super(PlaylistProxy, self).__init__()
        core_attrs = ['session_id']
        self._object_type = 'playlist'
        if session_id:
            self.session_id=session_id
        else:
            buckets = buckets or []
            kwargs['bucket'] = buckets
            kwargs['genre'] = kwargs['genres']
            del kwargs['genres']
            kwargs = dict((str(k), v) for (k,v) in kwargs.iteritems())
            
            if not all(ca in kwargs for ca in core_attrs):
                kwargs = dict((str(k), v) for (k,v) in kwargs.iteritems())
                profile = self.get_attribute('create', **kwargs)
                kwargs.update(profile)
            [self.__dict__.update({ca:kwargs.pop(ca)}) for ca in core_attrs if ca in kwargs]
            self.cache.update(kwargs)
        
    def get_attribute(self, method, **kwargs):
        return super(PlaylistProxy, self).get_attribute('dynamic/' + method, **kwargs)

class SongProxy(GenericProxy):
    def __init__(self, identifier, buckets = None, **kwargs):
        super(SongProxy, self).__init__()
        buckets = buckets or []
        self.id = identifier
        self._object_type = 'song'
        kwargs = dict((str(k), v) for (k,v) in kwargs.iteritems())
        
        # BAW -- this is debug output from identify that returns a track_id. i am not sure where else to access this..
        if kwargs.has_key("track_id"):
            self.track_id = kwargs["track_id"]
        if kwargs.has_key("tag"):
            self.tag = kwargs["tag"]
        if kwargs.has_key("score"):
            self.score = kwargs["score"]
        if kwargs.has_key('audio'):
            self.audio = kwargs['audio']
        if kwargs.has_key('release_image'):
            self.release_image = kwargs['release_image']
        
        # the following are integral to all song objects... the rest is up to you!
        core_attrs = ['title', 'artist_name', 'artist_id']
        
        if not all(ca in kwargs for ca in core_attrs):
            profile = self.get_attribute('profile', **{'id':self.id, 'bucket':buckets})
            kwargs.update(profile.get('songs')[0])
        [self.__dict__.update({ca:kwargs.pop(ca)}) for ca in core_attrs]
        self.cache.update(kwargs)
    
    def get_attribute(self, *args, **kwargs):
        kwargs['id'] = self.id
        return super(SongProxy, self).get_attribute(*args, **kwargs)
    

class TrackProxy(GenericProxy):
    def __init__(self, identifier, md5, properties):
        """
        You should not call this constructor directly, rather use the convenience functions
        that are in track.py. For example, call track.track_from_filename
        Let's always get the bucket `audio_summary`
        """
        super(TrackProxy, self).__init__()
        self.id = identifier
        self.md5 = md5
        self.analysis_url = None
        self._object_type = 'track'
        self.__dict__.update(properties)
    
