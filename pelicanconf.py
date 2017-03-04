#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import pelican

AUTHOR = 'Oli Pratt'
SITENAME = AUTHOR

# Use document-relative URLs when developing.
SITEURL = 'http://localhost:8000'
RELATIVE_URLS = True

PATH = 'content'

# Localisation settings.
TIMEZONE = 'Europe/London'
# Open Graph locale.
OG_LOCALE = 'en_GB'
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

THEME = "../pelican-themes/Flex"
BROWSER_COLOR = '#282828'

SITETITLE = AUTHOR
SITESUBTITLE = 'Software Engineer'
SITEDESCRIPTION = '%s\'s Thoughts and Writings' % AUTHOR
SITELOGO = '/static/images/site_logo.png'
FAVICON = '/favicon.ico'

MAIN_MENU = True
MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

# Use monokai for code snippets, and set a CSS file which sets any unstyled
# text in a code block to match plain text - otherwise it's black and
# unreadable.
PYGMENTS_STYLE = 'monokai'
CUSTOM_CSS = 'static/custom.css'

# Static files config.
STATIC_PATHS = ['static']
EXTRA_PATH_METADATA = {
    'static/robots.txt': {'path': 'robots.txt'},
    'static/images/favicon.ico': {'path': 'favicon.ico'},
    'static/CNAME': {'path': 'CNAME'},
}

# Don't add authors page or author directory - there's only ever one author.
AUTHORS_SAVE_AS = ''
AUTHOR_SAVE_AS = ''

# Delete output directory when building, but retain git data.
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = ['.git']

# Replacements for strings with special characters that can't appear in slugs.
SLUG_SUBSTITUTIONS = (('C++', 'cpp'),)

# Enable selected plugins.
PLUGIN_PATHS = ['../pelican-plugins/']
PLUGINS = ['sitemap', 'post_stats', 'representative_image']

# Sitemap config.
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.6,
        'pages': 0.5,
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'daily',
        'pages': 'monthly',
    }
}

ROBOTS = 'index, follow'

# Don't list tags against articles on the homepage.
HOME_HIDE_TAGS = True

# Add the TOC Markdown extenstion so headings have links added automatically.
# Needs all other default settings added or they are lost, so import those
# from the Pelican default config dict and then update it.
MARKDOWN = pelican.settings.DEFAULT_CONFIG['MARKDOWN']
MARKDOWN['extension_configs'].update({'markdown.extensions.toc': {}})
