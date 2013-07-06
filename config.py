#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
global configuration
version 1.0
history:
2013-6-19    dylanninin@gmail.com    init
"""

import web

blogconfig = web.storage(
    name = 'Pastime Paradise',
    home = 'http://dylanninin.com:8080',
    author = 'dylan',
    disqus = '"webpymdblog"',
    google_analytics = '"UA-21870463-1"',
    template_dir = 'template',
    entry_dir = 'raw/entry',
    page_dir = 'raw/page',
    tweet_dir = 'raw/tweet',
    static_dir = 'static',
    url_suffix = '.html',
    raw_suffix = '.md',
    index_url = '/',
    entry_url = '/blog',
    tweet_url = '/tweet',
    archive_url = '/archive',
    about_url = '/about.html',
    subscribe_url = '/atom.xml',
    error_url = '/error.html',
    favicon_url = '/favicon.ico',
    search_url = '/search',
    static_url = '/static',
    raw_url = '/raw',
    other_url = '(.+)',
    start = 1,
    limit = 5,
    pagination = 15,
    search_holder = 'search all site',
    time_fmt = '%Y-%m-%d %H:%M:%S',
    date_fmt = '%Y-%m-%d',
    url_fmt = 'yyyy/mm/dd',
    url_date_fmt = '%Y/%m/%d',
    recently = 10,
    ranks = 10,
    subscribe = 10,
    cache = False,
    debug = True,
)

web.config.debug = blogconfig.debug
render = web.template.render(blogconfig.template_dir, cache=blogconfig.cache)
web.template.Template.globals['config'] = blogconfig
web.template.Template.globals['render'] = render

urls = (
    blogconfig.index_url + '/?', 'controller.Index',
    blogconfig.entry_url + '(.*)','controller.Entry',
    blogconfig.archive_url + '(.*)', 'controller.Archive',
    blogconfig.about_url, 'controller.About',
    blogconfig.subscribe_url, 'controller.Subscribe',
    blogconfig.search_url + '?(.+)','controller.Search',
    blogconfig.raw_url + '(.*)','controller.Raw',
    blogconfig.favicon_url, 'controller.Image',
    blogconfig.other_url, 'controller.Error',
)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
