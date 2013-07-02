#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for the entry, page, templates, modules
version 1.0
history:
2013-6-19    dylanninin@gmail.com    init
"""

import calendar
from datetime import datetime
from config import blogconfig as config
from tool import Dict2Object


class Models: 
    """
    Models
    """
    def params(self):
        model ={
            'entries':None,
            'entry':None,
            'pager':None,
            'archive':None,
            'search':None,
            'subscribe':None,
            'error':None,
            'primary':{
                'abouts':None,
                'tags':None,
                'recently_entries':None,
            },
            'secondary':{
                'categories':None,
                'archive':None
            }
        }
        return Dict2Object(model)
        
    def entry(self, entry_type):
        model = {
                 'author':{
                        'name':config.author,
                        'url':config.home
                           },
                 'path':'the path of the entry',
                 'name':'the displayed name of the entry',
                 'raw_url':'the url of the raw format of this entey',
                 'url':'the url of the entry in this blog',
                 'type':entry_type,
                 'status':'published',
                 'time':None,
                 'date':None,
                 'excerpt':'the excerpt of the entry',
                 'content':'the content of the entry',
                 'html':'the html content of the entry',
                 'tags':[],
                 'categories':[],
                 'count':0,
                 'raw_count':0
        }
        return Dict2Object(model)
    
    def search(self, search_type, value, total):
        model = {
            'type':search_type,
            'value':value,
            'title':str(total)+ ' ' + self.plurals('result', total) + ' matching "' + value + '" of ' + search_type
        }
        return  Dict2Object(model)
    
    def pager(self, pager_type, value, total=0, pages=1, start=config.start, limit=config.limit):
        model ={
            'type':pager_type,
            'value':value,
            'total':total,
            'pages':pages,
            'start':start,
            'limit':limit,
            'pagination':[i for i in xrange(1, pages + 1)]
        }
        return Dict2Object(model)
    
    def archive(self, archive_type, archive_url, display, url, count=1):
        title = 'Archive ' + str(count) + ' '  +  self.plurals(archive_type, count) + ' of ' + display
        model = {
            'type':archive_type,
            'url':archive_url,
            'display':display,
            'title':title,
            'urls':[url],
            'count':count
        }
        return  Dict2Object(model)
    
    def subscribe(self, time):
        model = {
            'updated': time
        }
        return Dict2Object(model)
    
    def error(self, code='404', url=''):
        model = {
            'title': code + ' Not Found',
            'url':url,
            'statusCode':code,
            'message':'Oops! The requested url "' + url + '" could not be found...'
        }
        return Dict2Object(model)
    
    def about(self, about_type, prev_url=None, prev_name=None, next_url=None, next_name=None):
        model = {
            'type':about_type,
            'display':about_type.title(),
            'prev_url':prev_url,
            'prev_name':prev_name,
            'next_url':next_url,
            'next_name':next_name
        }
        return Dict2Object(model)
    
    def tag(self, tag, url):
        model = {
            'name':tag,
            'count':1,
            'rank':1,
            'urls':[url]
        }
        return  Dict2Object(model)

    def category(self, category, url):
        model = {
            'name':category,
            'count':1,
            'rank':1,
            'subs':[],
            'urls':[url]
        } 
        return  Dict2Object(model)

    def calendar(self, date):
        calendar.setfirstweekday(calendar.SUNDAY)
        ym = date[:len('yyyy-mm')]
        y, m, _ = [int(i) for i in date.split('-')]
        _, n = calendar.monthrange(y, m)
        urls = [None for _ in range(0, n + 1)]
        urls[0] = ''
        model = {
            'month':ym,
            'display':datetime(int(y), int(m), 1).strftime('%B %Y'),
            'days':calendar.monthcalendar(y, m),
            'urls':urls,
            'counts':[0 for _ in range(0, n+1)]
        }
        return Dict2Object(model)
    
    def monthly_archive(self, archive_type, month, url):
        y, m , _ = month.split('/')
        display = datetime(int(y), int(m), 1).strftime('%B %Y')
        archive_url = config.archive_url + '/' +  month
        return  self.archive(archive_type, archive_url, display, url, 1)
    
    def plurals(self, key, count=0):
        words = {
            'entry':'entries',
            'raw':'raws',
            'tag':'tags',
            'category':'categories',
            'result':'results'
        }
        if count > 1 and not words.get(key) == None:
            return words.get(key)
        return key
    
    def types(self):
        model = {
        'blog':'blog',
        'entry':'entry',
        'page':'page',
        'raw':'raw',
        'query':'query',
        'tag':'tag',
        'category':'category',
        'index':'index',
        'add':'add',
        'delete':'delete',
        'archive':'archive',
        'all':'all'
        }
        return Dict2Object(model)

if __name__ == '__main__':
    import doctest
    doctest.testmod()