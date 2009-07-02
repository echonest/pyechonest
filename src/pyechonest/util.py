#!/usr/bin/env python
# encoding: utf-8
"""
Utility functions to support the Echo Nest web API interface.  This
module is not meant for other uses and should not be used unless
modifying or extending the package.
"""

import time
import urllib
import urllib2
import xml.dom.minidom
from xml.etree.ElementTree import fromstring

from pyechonest import config
import urllib2_file


SUCCESS_STATUS_CODES = ( 0, )
FAILURE_THING_ID_STATUS_CODES = (7, 6)
FAILURE_API_KEY_STATUS_CODES = (12,)

CALL_LOG = []

def parse_http_response(response):
    return check_status(fromstring(response))

def call(method, params, POST=False):
    if not check_call_log():
        # raise some kind of error
        raise EchoNestAPIError(1,"Rate limit exceeded. You've already made "\
                                "120 API calls in the last minute.")
    params.update({'api_key': config.ECHO_NEST_API_KEY, 'version': 3})
    params = urllib.urlencode(params)
    if(POST):
        url = 'http://%s%s%s' % (config.API_HOST, config.API_SELECTOR, method)
        f = urllib.urlopen(url, params)
    else:
        url = 'http://%s%s%s?%s' % (config.API_HOST, config.API_SELECTOR, 
                                    method, params)
        f = urllib.urlopen(url)
    return parse_http_response(f.read())

def check_call_log():
    global CALL_LOG
    CALL_LOG = filter(lambda x: x > (time.time() - 60), CALL_LOG)
    if len(CALL_LOG) >= 120:
        return False
    CALL_LOG.append(time.time())
    return True

def check_status(etree):
    code = int(etree._children[0]._children[0].text)
    message = etree._children[0]._children[1].text
    if code!=0:
        raise EchoNestAPIError(code, message)
    else:
        return etree


class EchoNestAPIError(Exception):
    """
    Generic API errors. 
    """
    def __init__(self, code, message):
        self.code = code
        self._message = message
    def __str__(self):
        return repr(self)
    def __repr__(self):
        return 'Echo Nest API Error %d: %s' % (self.code, self._message)


class EchoNestAPIKeyError(EchoNestAPIError):
    """
    An Error returned by the API regarding the API Key. 
    """
    pass


class EchoNestAPIThingIDError(EchoNestAPIError):
    """
    An Error returned by the API regarding the ThingID. 
    """
    pass


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
    
    

    
    
    