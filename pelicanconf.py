#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Oli Pratt'
SITENAME = 'Oli Pratt'
SITEURL = ''

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
SOCIAL = (('github', 'https://github.com/olipratt'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "../pelican-themes/Flex"

SITETITLE = 'Oli Pratt'
SITESUBTITLE = 'Sotfware Engineer'
SITEDESCRIPTION = '%s\'s Thoughts and Writings' % AUTHOR
SITELOGO = 'static/images/site_logo.png'
FAVICON = SITEURL + 'static/images/favicon.ico'

MAIN_MENU = True
MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

PYGMENTS_STYLE = 'monokai'
STATIC_PATHS = ['static']

