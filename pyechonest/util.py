#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2010-04-25.

Utility functions to support the Echo Nest web API interface.
"""
import urllib
import urllib2
import httplib
import config
import logging
import socket
import re
import time
import os
import subprocess
import traceback
from types import StringType, UnicodeType

try:
    import json
except ImportError:
    import simplejson as json

logger = logging.getLogger(__name__)
TYPENAMES = (
    ('AR', 'artist'),
    ('SO', 'song'),
    ('RE', 'release'),
    ('TR', 'track'),
    ('PE', 'person'),
    ('DE', 'device'),
    ('LI', 'listener'),
    ('ED', 'editor'),
    ('TW', 'tweditor'),
    ('CA', 'catalog'),
)
foreign_regex = re.compile(r'^.+?:(%s):([^^]+)\^?([0-9\.]+)?' % r'|'.join(n[1] for n in TYPENAMES))
short_regex = re.compile(r'^((%s)[0-9A-Z]{16})\^?([0-9\.]+)?' % r'|'.join(n[0] for n in TYPENAMES))
long_regex = re.compile(r'music://id.echonest.com/.+?/(%s)/(%s)[0-9A-Z]{16}\^?([0-9\.]+)?' % (r'|'.join(n[0] for n in TYPENAMES), r'|'.join(n[0] for n in TYPENAMES)))
headers = [('User-Agent', 'Pyechonest %s' % (config.__version__,))]

class MyBaseHandler(urllib2.BaseHandler):
    def default_open(self, request):
        if config.TRACE_API_CALLS:
            logger.info("%s" % (request.get_full_url(),))
        request.start_time = time.time()
        return None
        
class MyErrorProcessor(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        code = response.code
        if config.TRACE_API_CALLS:
            logger.info("took %2.2fs: (%i)" % (time.time()-request.start_time,code))
        if code/100 in (2, 4, 5):
            return response
        else:
            urllib2.HTTPErrorProcessor.http_response(self, request, response)

opener = urllib2.build_opener(MyBaseHandler(), MyErrorProcessor())
opener.addheaders = headers

class EchoNestException(Exception):
    """
    Parent exception class.  Catches API and URL/HTTP errors.
    """
    def __init__(self, code, message, headers):
        if code is None:
            code = -1
            message = 'Echo Nest Unknown Error'

        if message is None:
            super(EchoNestException, self).__init__('Echo Nest Error %d' % code,)
        else:
            super(EchoNestException, self).__init__(message,)
        self.headers = headers
        self.code = code

class EchoNestAPIError(EchoNestException):
    """
    API Specific Errors.
    """
    def __init__(self, code, message, headers, http_status):
        if http_status:
            http_status_message_part = ' [HTTP %d]' % http_status
        else:
            http_status_message_part = ''
        self.http_status = http_status

        formatted_message = ('Echo Nest API Error %d: %s%s' %
                             (code, message, http_status_message_part),)
        super(EchoNestAPIError, self).__init__(code, formatted_message, headers)

class EchoNestIOError(EchoNestException):
    """
    URL and HTTP errors.
    """
    def __init__(self, code=None, error=None, headers=headers):
        formatted_message = ('Echo Nest IOError: %s' % headers,)
        super(EchoNestIOError, self).__init__(code, formatted_message, headers)

def get_successful_response(raw_json):
    if hasattr(raw_json, 'headers'):
        headers = raw_json.headers
    else:
        headers = {'Headers':'No Headers'}
    if hasattr(raw_json, 'getcode'):
        http_status = raw_json.getcode()
    else:
        http_status = None
    raw_json = raw_json.read()
    try:
        response_dict = json.loads(raw_json)
        status_dict = response_dict['response']['status']
        code = int(status_dict['code'])
        message = status_dict['message']
        if (code != 0):
            # do some cute exception handling
            raise EchoNestAPIError(code, message, headers, http_status)
        del response_dict['response']['status']
        return response_dict
    except ValueError:
        logger.debug(traceback.format_exc())
        raise EchoNestAPIError(-1, "Unknown error.", headers, http_status)


def callm(method, param_dict, POST=False, socket_timeout=None, data=None):
    """
    Call the api! 
    Param_dict is a *regular* *python* *dictionary* so if you want to have multi-valued params
    put them in a list.
    
    ** note, if we require 2.6, we can get rid of this timeout munging.
    """
    try:
        param_dict['api_key'] = config.ECHO_NEST_API_KEY
        param_list = []
        if not socket_timeout:
            socket_timeout = config.CALL_TIMEOUT

        for key,val in param_dict.iteritems():
            if isinstance(val, list):
                param_list.extend( [(key,subval) for subval in val] )
            elif val is not None:
                if isinstance(val, unicode):
                    val = val.encode('utf-8')
                param_list.append( (key,val) )

        params = urllib.urlencode(param_list)

        orig_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(socket_timeout)

        if(POST):
            if (not method == 'track/upload') or ((method == 'track/upload') and 'url' in param_dict):
                """
                this is a normal POST call
                """
                url = 'http://%s/%s/%s/%s' % (config.API_HOST, config.API_SELECTOR,
                                            config.API_VERSION, method)

                if data is None:
                    data = ''
                data = urllib.urlencode(data)
                data = "&".join([data, params])

                f = opener.open(url, data=data)
            else:
                """
                upload with a local file is special, as the body of the request is the content of the file,
                and the other parameters stay on the URL
                """
                url = '/%s/%s/%s?%s' % (config.API_SELECTOR, config.API_VERSION,
                                            method, params)

                if ':' in config.API_HOST:
                    host, port = config.API_HOST.split(':')
                else:
                    host = config.API_HOST
                    port = 80

                if config.TRACE_API_CALLS:
                    logger.info("%s/%s" % (host+':'+str(port), url,))
                conn = httplib.HTTPConnection(host, port = port)
                conn.request('POST', url, body = data, headers = dict([('Content-Type', 'application/octet-stream')]+headers))
                f = conn.getresponse()

        else:
            """
            just a normal GET call
            """
            url = 'http://%s/%s/%s/%s?%s' % (config.API_HOST, config.API_SELECTOR, config.API_VERSION,
                                            method, params)

            f = opener.open(url)

        socket.setdefaulttimeout(orig_timeout)

        # try/except
        response_dict = get_successful_response(f)
        return response_dict

    except IOError, e:
        if hasattr(e, 'reason'):
            raise EchoNestIOError(error=e.reason)
        elif hasattr(e, 'code'):
            raise EchoNestIOError(code=e.code)
        else:
            raise

def oauthgetm(method, param_dict, socket_timeout=None):
    try:
        import oauth2 # lazy import this so oauth2 is not a hard dep
    except ImportError:
        raise Exception("You must install the python-oauth2 library to use this method.")

    """
    Call the api! With Oauth! 
    Param_dict is a *regular* *python* *dictionary* so if you want to have multi-valued params
    put them in a list.
    
    ** note, if we require 2.6, we can get rid of this timeout munging.
    """
    def build_request(url):
        params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': int(time.time())
            }
        consumer = oauth2.Consumer(key=config.ECHO_NEST_CONSUMER_KEY, secret=config.ECHO_NEST_SHARED_SECRET)
        params['oauth_consumer_key'] = config.ECHO_NEST_CONSUMER_KEY
        
        req = oauth2.Request(method='GET', url=url, parameters=params)
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        req.sign_request(signature_method, consumer, None)
        return req
    
    param_dict['api_key'] = config.ECHO_NEST_API_KEY
    param_list = []
    if not socket_timeout:
        socket_timeout = config.CALL_TIMEOUT
    
    for key,val in param_dict.iteritems():
        if isinstance(val, list):
            param_list.extend( [(key,subval) for subval in val] )
        elif val is not None:
            if isinstance(val, unicode):
                val = val.encode('utf-8')
            param_list.append( (key,val) )

    params = urllib.urlencode(param_list)
    
    orig_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(socket_timeout)
    """
    just a normal GET call
    """
    url = 'http://%s/%s/%s/%s?%s' % (config.API_HOST, config.API_SELECTOR, config.API_VERSION, 
                                     method, params)
    req = build_request(url)
    f = opener.open(req.to_url())
            
    socket.setdefaulttimeout(orig_timeout)
    
    # try/except
    response_dict = get_successful_response(f)
    return response_dict


def postChunked(host, selector, fields, files):
    """
    Attempt to replace postMultipart() with nearly-identical interface.
    (The files tuple no longer requires the filename, and we only return
    the response body.) 
    Uses the urllib2_file.py originally from 
    http://fabien.seisen.org which was also drawn heavily from 
    http://code.activestate.com/recipes/146306/ .
    
    This urllib2_file.py is more desirable because of the chunked 
    uploading from a file pointer (no need to read entire file into 
    memory) and the ability to work from behind a proxy (due to its 
    basis on urllib2).
    """
    params = urllib.urlencode(fields)
    url = 'http://%s%s?%s' % (host, selector, params)
    u = urllib2.urlopen(url, files)
    result = u.read()
    [fp.close() for (key, fp) in files]
    return result


def fix(x):
    # we need this to fix up all the dict keys to be strings, not unicode objects
    assert(isinstance(x,dict))
    return dict((str(k), v) for (k,v) in x.iteritems())


def map_idspace(input_idspace):
    if input_idspace == 'spotify-WW' or input_idspace == 'spotifyv2-ZZ':
        return 'spotify'
    return input_idspace
