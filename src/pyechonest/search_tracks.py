#!/usr/bin/env python
# encoding: utf-8
"""
A Python interface to the The Echo Nest's web API.  See
http://developer.echonest.com/ for details.
"""

import util
try:
    import json
except ImportError:
    import simplejson as json

def search_tracks(artist=None, title=None, sort=None, query=None):
    response = util.call('alpha_search_tracks', {'query':query, 'sort':sort }, check_status=False)
    return json.loads(response)
