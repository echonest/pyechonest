#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2011-10-21.

The Sandbox module loosely covers http://developer.echonest.com/docs/v4/sandbox.html
Refer to the official api documentation if you are unsure about something.
"""
try:
    import json
except ImportError:
    import simplejson as json
import datetime

import util
from proxies import ResultList

def list(sandbox_name, results=15, start=0):
    """
    Returns a list of all assets available in this sandbox
    
    Args:
        sandbox_name (str): A string representing the name of the sandbox

    Kwargs:
        results (int): An integer number of results to return
        
        start (int): An integer starting value for the result set
        
    Returns:
        A list of asset dictionaries
    
    Example:

    >>> sandbox.list('bluenote')
    [{}, {}]
    >>> 

    
    """
    result = util.callm("%s/%s" % ('sandbox', 'list'), {'sandbox':sandbox_name, 'results': results, 'start': start})
    assets = result['response']['assets']
    start = result['response']['start']
    total = result['response']['total']

    return ResultList(assets, start, total)
    

def access(sandbox_name, asset_ids):
    """
    Returns a list of assets with expiring access urls that can be used to download them
    *Requires Oauth*

    Args:
        sandbox_name (str): A string representing the name of the sandbox
        asset_ids (list): A list of asset_ids (str) to fetch

    Kwargs:
        
    Returns:
        A list of asset dictionaries
    
    Example:

    >>> sandbox.access('bluenote', ['12345'])
    [{}, {}]
    >>> 

    
    """
    result = util.oauthgetm("%s/%s" % ('sandbox', 'access'), {'sandbox':sandbox_name, 'id':asset_ids})
    return  result['response']['assets']
    
