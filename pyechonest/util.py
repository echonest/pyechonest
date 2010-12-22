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

logging.basicConfig(level=logging.INFO)
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
        if code in [200, 400, 403, 500]:
            return response
        else:
            urllib2.HTTPErrorProcessor.http_response(self, request, response)

opener = urllib2.build_opener(MyBaseHandler(), MyErrorProcessor())
opener.addheaders = headers

class EchoNestAPIError(Exception):
    """
    Generic API errors. 
    """
    def __init__(self, code, message):
        self.args = ('Echo Nest API Error %d: %s' % (code, message),)

def get_successful_response(raw_json):
    try:
        response_dict = json.loads(raw_json)
        status_dict = response_dict['response']['status']
        code = int(status_dict['code'])
        message = status_dict['message']
        if (code != 0):
            # do some cute exception handling
            raise EchoNestAPIError(code, message)
        del response_dict['response']['status']
        return response_dict
    except ValueError:
        logger.debug(traceback.format_exc())
        raise EchoNestAPIError(-1, "Unknown error.")


# These two functions are to deal with the unknown encoded output of codegen (varies by platform and ID3 tag)
def reallyunicode(s, encoding="utf-8"):
    if type(s) is StringType:
        for args in ((encoding,), ('utf-8',), ('latin-1',), ('ascii', 'replace')):
            try:
                s = s.decode(*args)
                break
            except UnicodeDecodeError:
                continue
    if type(s) is not UnicodeType:
        raise ValueError, "%s is not a string at all." % s
    return s

def reallyUTF8(s):
    return reallyunicode(s).encode("utf-8")

def codegen(filename, start=0, duration=30):
    # Run codegen on the file and return the json. If start or duration is -1 ignore them.
    cmd = config.CODEGEN_BINARY_OVERRIDE
    if not cmd:
        # Is this is posix platform, or is it windows?
        if hasattr(os, 'uname'):
            if(os.uname()[0] == "Darwin"):
                cmd = "codegen.Darwin"
            else:
                cmd = 'codegen.'+os.uname()[0]+'-'+os.uname()[4]
        else:
            cmd = "codegen.windows.exe"

    if not os.path.exists(cmd):
        raise Exception("Codegen binary not found.")

    command = cmd + " \"" + filename + "\" " 
    if start >= 0:
        command = command + str(start) + " "
    if duration >= 0:
        command = command + str(duration)
        
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (json_block, errs) = p.communicate()
    json_block = reallyUTF8(json_block)

    try:
        return json.loads(json_block)
    except ValueError:
        logger.debug("No JSON object came out of codegen: error was %s" % (errs))
        return None


def callm(method, param_dict, POST=False, socket_timeout=None, data=None):
    """
    Call the api! 
    Param_dict is a *regular* *python* *dictionary* so if you want to have multi-valued params
    put them in a list.
    
    ** note, if we require 2.6, we can get rid of this timeout munging.
    """
    param_dict['api_key'] = config.ECHO_NEST_API_KEY
    param_list = []
    if not socket_timeout:
        socket_timeout = config.CALL_TIMEOUT
    
    for key,val in param_dict.iteritems():
        if isinstance(val, list):
            param_list.extend( [(key,subval) for subval in val] )
        else:
            if isinstance(val, unicode):
                val = val.encode('utf-8')
            param_list.append( (key,val) )

    params = urllib.urlencode(param_list)
        
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
            
    socket.setdefaulttimeout(None)
    
    # try/except
    response_dict = get_successful_response(f.read())
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

