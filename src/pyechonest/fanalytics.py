#!/usr/bin/env python
# encoding: utf-8
"""
A Python interface to the The Echo Nest's web API.  See
http://developer.echonest.com/ for details.
"""

import config
import document
import util as util

from elementtree.ElementTree import Element, SubElement, dump

config.TRACE_API_CALLS = True
config.API_HOST = 'developer2.echonest.com'

def get_blog_terms(blogs = [], refresh=False):
    """Return a list of weighted musical terms (styles, genres) that
    describe the type of music that the blog covers. """

    params = []
    for b in blogs:
        params.append(('blog_url', b))
    results = util.callm('get_blog_terms', params)
    bloglist = results.findall('blogs/blog')
    results = []
    for i,b in enumerate(bloglist):
        result = {}
        result['url'] = b.attrib['url']
        result['requested_url'] = blogs[i]
        terms = []
        for term in b.findall('terms'):
            score = term.attrib['score']
            name = term.text
            terms.append( (name, score))
        result['terms'] = terms
        results.append(result)
        print results
    return results

if __name__ == "__main__":
   # get_blog_terms(blogs=['http://music.for-robots.com', 'http://www.fluxblog.org'])
    get_blog_terms(blogs=['http://music.for-robots.com', 'http://fluxblog.org', 'http://echonest.com'])
    
