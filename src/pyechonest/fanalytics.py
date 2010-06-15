#!/usr/bin/env python
# encoding: utf-8
"""
A Python interface to the The Echo Nest's web API.  See
http://developer.echonest.com/ for details.
"""
import util

def get_blog_terms(blogs = None, refresh=False):
    """  Return a list of weighted musical terms (styles, genres) that
         describe the type of music that the blog covers. 
    """

    blogs = blogs or []
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
    return results

if __name__ == "__main__":
    print get_blog_terms(blogs=['http://music.for-robots.com', 'http://fluxblog.org', 
        'http://echonest.com'])
    
