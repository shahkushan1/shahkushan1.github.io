#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import socket

AUTHOR = u'Kushan Shah'
SITENAME = u'Kushan Shah'
SITEURL = 'http://www.kushanshah.in' if socket.gethostbyname(socket.gethostname()) == "127.0.1.1" else "http://localhost:8000"

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
USER_LOGO_URL = SITEURL + '/static/images/kushan.png'

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}