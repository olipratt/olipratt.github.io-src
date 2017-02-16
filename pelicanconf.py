#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Oli Pratt'
SITENAME = AUTHOR
SITEURL = 'http://localhost:8000'

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'English'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Metaswitch', 'https://www.metaswitch.com/'),)

# Social widget
SOCIAL = (('github', 'https://github.com/olipratt'),
          ('rss', '/feeds/all.atom.xml'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = "../pelican-themes/Flex"

SITETITLE = AUTHOR
SITESUBTITLE = 'Software Engineer'
SITEDESCRIPTION = '%s\'s Thoughts and Writings' % AUTHOR
SITELOGO = '/static/images/site_logo.png'
FAVICON = '/static/images/favicon.ico'

MAIN_MENU = True
MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

PYGMENTS_STYLE = 'monokai'
STATIC_PATHS = ['static']

# Don't add authors page or author directory - there's only ever one author.
AUTHORS_SAVE_AS = ''
AUTHOR_SAVE_AS = ''

# Delete output directory when building, but retain git and CNAME data.
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = ['.git', 'CNAME']

# Replacements for strings with special characters that can't appear in slugs.
SLUG_SUBSTITUTIONS = (('C++', 'cpp'),)
