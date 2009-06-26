#!/usr/bin/env python
# encoding: utf-8
"""
document.py

Created by Ben Lacker on 2009-06-25.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import math
import urllib

from pyechonest import config
from pyechonest.util import call

class DocumentSetCache(object):
    def __init__(self, document_set, identifier, method):
        self._cache = {}
        self.chunk_size = 15
        self.document_set = document_set
        self.extra_params = {}
        self.identifier = identifier
        self.method = method
    
    def __getitem__(self, k):
        if not isinstance(k, (int, long)):
            raise TypeError
        if not self._cache.has_key(k):
            params = {'id': self.identifier, 'start': k * self.chunk_size, 'rows': self.chunk_size}
            params.update(self.extra_params)
            self._cache[k] = call(self.method, params)
        return self._cache[k]
    
    def __iter__(self):
        return (self[i] for i in xrange(len(self)))
    
    def __len__(self):
        return math.ceil(len(self.document_set) / float(self.chunk_size))


class DocumentSet(object):
    def __init__(self, identifier, method, element_path):
        self._cache = DocumentSetCache(self, identifier, method)
        self._len = None
        self.identifier = identifier
        self.method = method
        self.element_path = element_path
    
    def __getitem__(self, k):
        chunk_and_index = lambda i: (i / self._cache.chunk_size, i % self._cache.chunk_size)
        if isinstance(k, (int, long)):
            chunk, index = chunk_and_index(k)
            return self._parse_element(self._cache[chunk].findall(self.element_path)[index])
        elif not isinstance(k, slice):
            raise TypeError
        start = k.start or 0
        start_chunk, start_index = chunk_and_index(start)
        stop = min(k.stop or len(self), len(self)) - 1 # use inclusive to simplify logic
        stop_chunk, stop_index = chunk_and_index(stop)
        items = []
        for chunk in xrange(start_chunk, stop_chunk + 1):
            elements = self._cache[chunk].findall(self.element_path)
            if chunk == start_chunk and chunk == stop_chunk:
                elements = elements[start_index:stop_index + 1]
            elif chunk == start_chunk:
                elements = elements[start_index:]
            elif chunk == stop_chunk:
                elements = elements[:stop_index + 1]
            items.extend([self._parse_element(e) for e in elements])
        return items
    
    def __iter__(self):
        for chunk in iter(self._cache):
            for element in chunk.findall(self.element_path):
                yield self._parse_element(element)
    
    def __len__(self):
        if self._len is None:
            first_chunk = self._cache._cache.itervalues().next() if len(self._cache._cache) else self._cache[0]
            self._len = int(first_chunk.find(self.element_path.split('/')[0]).get('found'))
        return self._len
    
    def _parse_element(self, element):
        return element


class WebDocumentSet(DocumentSet):
    def __init__(self, identifier, method):
        super(WebDocumentSet, self).__init__(identifier, method, 'results/doc')
    
    def _parse_element(self, element):
        parsed = dict((e.tag, e.text) for e in element.getchildren())
        if element.attrib.has_key('id'):
            parsed.update({'id': element.attrib['id']})
        return parsed

