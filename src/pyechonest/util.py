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
try:
    from xml.etree.cElementTree import fromstring
except ImportError:
    from xml.etree.ElementTree import fromstring


import config
import urllib2_file


SUCCESS_STATUS_CODES = ( 0, )
FAILURE_THING_ID_STATUS_CODES = (7, 6)
FAILURE_API_KEY_STATUS_CODES = (12,)

CALL_LOG = []

def parse_http_response(response):
    response = fromstring(response)
    return check_status(response)

def call(method, params, POST=False, buckets=[]):
    rate_limit_exceeded = not check_call_log()
    while rate_limit_exceeded:
        time.sleep(0.5)
        rate_limit_exceeded = not check_call_log()
    params.update({'api_key': config.ECHO_NEST_API_KEY, 'version': 3})
    for k,v in params.items():
        if isinstance(v, unicode):
            params[k] = v.encode('utf-8')
    params = urllib.urlencode(params)
    if(POST):
        url = 'http://%s%s%s' % (config.API_HOST, config.API_SELECTOR, method)
        f = urllib.urlopen(url, params)
    else:
        url = 'http://%s%s%s?%s' % (config.API_HOST, config.API_SELECTOR, 
                                    method, params)
        # hack to add buckets
        for bucket in buckets:
            url += '&bucket='+bucket
        f = urllib.urlopen(url)
    if config.TRACE_API_CALLS:
        print url
    response = fromstring(f.read())
    return check_status(response)

def check_call_log():
    if not config.OBEY_RATE_LIMIT:
        return True
    global CALL_LOG
    CALL_LOG = filter(lambda x: x > (time.time() - 60), CALL_LOG)
    if len(CALL_LOG) >= 120:
        return False
    CALL_LOG.append(time.time())
    return True

def check_status(etree):
    code = int(etree.getchildren()[0].getchildren()[0].text)
    message = etree.getchildren()[0].getchildren()[1].text
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
    
