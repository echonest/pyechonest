#!/usr/bin/env python
# encoding: utf-8
"""
Utility functions to support the Echo Nest web API interface.  This
module is not meant for other uses and should not be used unless
modifying or extending the package.
"""


import urllib

from xml.etree.ElementTree import fromstring

from pyechonest import config

SUCCESS_STATUS_CODES = ( 0, )
FAILURE_THING_ID_STATUS_CODES = (7, 6)
FAILURE_API_KEY_STATUS_CODES = (12,)


def call(method, params): 
    params.update({'api_key': config.API_KEY, 'version': 3})
    params = urllib.urlencode(params)
    url = 'http://%s%s%s?%s' % (config.API_HOST, config.API_SELECTOR, method, params)
    f = urllib.urlopen(url)
    return check_status(fromstring(f.read()))


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

