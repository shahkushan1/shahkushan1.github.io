# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Kushan Shah'
SITENAME = u'Kushan Shah'
SITEURL = 'http://www.kushanshah.in'

PATH = 'content'

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
# LINKS = (('About', 'http://kushanshah.in/about'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/shahkushan1'),
          ('LinkedIn', 'http://in.linkedin.com/in/kushanshah'),)

DEFAULT_PAGINATION = 10

THEME = 'pelican-svbhack'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

USER_LOGO_URL = SITEURL + '/images/kushan.png'

STATIC_PATHS = ['images', 'extras/CNAME']
EXTRA_PATH_METADATA = {'extras/CNAME': {'path': 'CNAME'}}

# Order archives by newest first by date
NEWEST_FIRST_ARCHIVES = True

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'

# Article URL and save location
ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{slug}/index.html'

# Page URL and save location
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'