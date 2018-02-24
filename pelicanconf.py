#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import pelican


# - High level site settings.
# High level strings.
AUTHOR = 'Oli Pratt'
SITENAME = AUTHOR
SITETITLE = AUTHOR
COPYRIGHT_NAME = AUTHOR
SITESUBTITLE = 'Software Engineer'
SITEDESCRIPTION = '%s\'s Thoughts and Writings' % AUTHOR

# How many posts per-page on the index pages.
DEFAULT_PAGINATION = 6

# How long the summary should be. The default is fine.
# SUMMARY_MAX_LENGTH = 50

# Don't add authors page or author directory - there's only ever one author.
AUTHORS_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
# These feeds aren't wanted at all for this site.
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Replacements for strings with special characters that can't appear in slugs.
SLUG_SUBSTITUTIONS = (('C++', 'cpp'),)

# Default values for 'robots' meta tag.
ROBOTS = 'index, follow'


# - Localisation settings.
TIMEZONE = 'Europe/London'
# Open Graph locale.
OG_LOCALE = 'en_GB'
DEFAULT_LANG = 'English'


# - These options are overridden when publishing.
# Use document-relative URLs when developing
SITEURL = 'http://localhost:8000'
RELATIVE_URLS = True
# Feed generation is usually not desired when developing.
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None


# - File/directory related settings.
# Location of all user content.
PATH = 'content'

# Static files config.
STATIC_PATHS = ['static']
EXTRA_PATH_METADATA = {
    'static/robots.txt': {'path': 'robots.txt'},
    'static/images/favicon.ico': {'path': 'favicon.ico'},
    'static/CNAME': {'path': 'CNAME'},
}

# Static image paths.
SITELOGO = '/static/images/site_logo.png'
FAVICON = '/favicon.ico'

# Delete output directory when building, but retain git data.
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = ['.git', '.gitmodules', '.gitignore', 'giveitarestoli']


# - Links config.
# Blogroll
LINKS = (('Metaswitch', 'https://www.metaswitch.com/'),)

# Social widget
SOCIAL = (('github', 'https://github.com/olipratt'),
          ('linkedin', 'https://www.linkedin.com/in/olipratt/'),
          ('rss', '/feeds/all.atom.xml'),)

# Main menu settings.
MAIN_MENU = True
MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)


# - Plugin configuration.
# Enable selected plugins.
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['sitemap', 'post_stats', 'representative_image', 'neighbors']

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


# - Markdown configuration.
# Add the TOC Markdown extenstion so headings have links added automatically.
# Needs all other default settings added or they are lost, so import those
# from the Pelican default config dict and then update it.
import pymdownx.emoji
MARKDOWN = pelican.settings.DEFAULT_CONFIG['MARKDOWN']
extensions = {'markdown.extensions.toc': {},
              'pymdownx.emoji': {"emoji_generator": pymdownx.emoji.to_alt}}
MARKDOWN['extension_configs'].update(extensions)


# - Theme specific options.
# Use the Flex theme.
THEME = "Flex"
# Colour of mobile browsers viewing the site.
BROWSER_COLOR = '#282828'
# Don't list tags against articles on the homepage.
HOME_HIDE_TAGS = True
# Use monokai for code snippets, and set a CSS file which sets any unstyled
# text in a code block to match plain text - otherwise it's black and
# unreadable.
PYGMENTS_STYLE = 'monokai'
CUSTOM_CSS = 'static/custom.css'
