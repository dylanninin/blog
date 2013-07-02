#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Blog handler for urls
version 1.0
history:
2013-6-19    dylanninin@gmail.com    init
"""

import os
import config
from __init__ import entryService

render = config.render
web = config.web
config = config.blogconfig

class Index:
    """
    Index Handler for /?
    example:
        /    
            request the index of this blog and list the first page of all
            entries of this blog from newest to oldest
            the default page size is 5 which is configured with config.limit
                
        /?start=1 
            equivalent with /
                
        /?start=1&limit=10
            request the second page with 10 entries
                
    template:
        template/index.html
        
    reference:
        config.py, model.py, service.py
    """
    def GET(self):
        params = web.input(start=config.start, limit=config.limit)
        limit = int(params.limit)
        start = int(params.start)
        params = entryService.search(entryService.types.index, config.index_url, '', start, limit)
        return render.index(params)


class Entry:
    """
    Entry Handler for /blog(.*)
        
    example:
        /blog
            the same as request /
                
        /blog/
            the same as request /blog/
                
        /blog/2013/06/20/webpy_introduction.html
            request entry with this url else error will be responsed
                
    template:
        template/entry.html, template/index.html

    reference:
        config.py, model.py, service.py
    """
    def GET(self, url):
        if not url in ['', '/']:
            url = config.entry_url + url
            params = entryService.find_by_url(entryService.types.entry, url)
            if params.entry == None:
                raise web.notfound(render.error(params))
            else:
                return render.entry(params)
        params = entryService.search(entryService.types.index, url)
        return render.index(params)


class Archive:
    """
    Archive Handler for /archive(.*)
    
    example:
        /archive
            request the archive of all posted entries on this blog
                
        /archive/
            the same as /archive
         
        /archive/2013
            request the archive of all posted entries on 2013
    
        /archive/2013/
            the same as /archive/2013
          
        /archive/2013/06
            request the archive of all posted entries on 2013/06
        
        /archive/2013/06/
            the same as /archive/2013/06
           
        /archive/2013/06/20
             request the archive of all posted entries 2013/06/20
          
        /archive/2013/06/20
            the same as /archive/2013/06/20
           
    template:
        template/archive.html
            
    reference:
        config.py, model.py, service.py
    """
    def GET(self, url):
        url= config.archive_url + url
        params = entryService.archive(entryService.types.entry, url)
        if params.entries == None:
            raise web.notfound(render.error(params))
        return render.archive(params)


class About:
    """
    Page Handler for /about.html
    
    template:
        template/entry.html
    
    reference:
        config.py, model.py, service.py
    """    
    def GET(self):
        url = config.about_url
        params = entryService.find_by_url(entryService.types.page, url)
        if params.entry == None:
            raise web.notfound(render.error(params))
        return render.entry(params)


class Subscribe:
    """
    Subscribe Handler for /atom.xml
    #TODO: FIXME: find related entries
    
    template:
        template/subscribe.xml
    
    reference:
        config.py, model.py, service.py
    """       
    def GET(self):
        params =  entryService.search(entryService.types.index, config.subscribe_url)
        web.header('Content-Type', 'text/xml')
        return render.atom(params)


class Search:
    """
    Search Handler for /search?type=type&value=value&start=start&limit=limit
    
    example:
        /search?type=query&value=input&start=1&limit=5
       
        /search?type=tag&value=webpy&start=1&limit=5
       
        /search?type=category&value=python
    
    template:
        template/search.html
        
    reference:
        config.py, model.py, service.py
    """
    def GET(self, url):
        params = web.input(type=entryService.types.query, value='',\
                           start=config.start, limit=config.limit)
        limit = int(params.limit)
        start = int(params.start)
        url = '%s/?type=%s&value=%s&start=%d&limit=%d' % (config.search_url, params.type, params.value, start, limit)
        params = entryService.search(params.type, url, params.value, start, limit)
        if not params.entries == None: 
            return render.search(params)
        raise web.notfound(render.error(params))

class Raw:
    """
    Raw Handler for /raw(.+)
    example:
        /raw
            request the archive of raw formats of all posted entries on this blog
                
        /raw/
            the same as /raw/
                
        /raw/2013/06/20/webpy_introduction.md
            request the raw content with url 2013/06/20/webpy_introduction.md
            and usually the rendered html url is 2013/06/20/webpy_introduction.html
                
        /raw/about.md
            request the raw content with url about.md its rendered html url is /abouts.html
                
    reference:
        config.py, model.py, service.py
    """
    def GET(self, url):
        url = config.raw_url + url
        raw = entryService.find_raw(url)
        if not raw == None:
            web.header('Context-Type', 'text/plain')
            web.header('Content-Encoding','utf-8')
            return raw
        params = entryService.archive(entryService.types.raw, url)
        if params.entries  == None:
            raise web.notfound(render.error(params))
        return render.archive(params)


class Image:
    """
    favicon.ico handler
        
    reference: 
        config.py
    """
    def GET(self):
        url = config.favicon_url
        name = url.lstrip('/')
        ext = name.split('.')[-1]
        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"
        }
        if name in os.listdir(config.static_dir):
            web.header('Content-Type', cType[ext])
            return open('%s/%s' %(config.static_dir, name), 'rb').read()
        params =  entryService.error(url)
        raise web.notfound(render.error(params))


class Error():
    
    """
    Error Handler for any other url
        
    template:
        template/error.html
        
    reference:
        config.py, model.py, service.py
    """
    def GET(self, url):
        params = entryService.error(url)
        #return render.error(params)
        raise web.notfound(render.error(params))


if __name__ == "__main__":
    import doctest
    doctest.testmod()