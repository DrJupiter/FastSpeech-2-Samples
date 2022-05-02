AUTHOR = 'Klaus Bentzen, Rune Nedergaard, Andreas Holme'
SITENAME = 'Ukraine-Russia War a Twitter Analysis'

# SET TO FALSE WHEN DEVELOPING
publish = True
if publish:
    SITEURL = 'https://drjupiter.github.io/comsci.github.io'
GITHUB_URL = 'https://github.com/DrJupiter/comsci.github.io'

PATH = 'content'

TIMEZONE = 'Europe/Copenhagen'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

ARTICLE_PATHS = ['articles']
#NEWEST_FIRST_ARCHIVES = False
ARTICLE_ORDER_BY = 'date'
THEME = 'attila'

"""
The following code adds Menus to the menu bar with the correct
title.
It is long, but it does what is suppossed to,... I think.

Also until I figure out the ordering of the articles on the main page 
as well as in the next and prev article, we are using a 1,2,3,4... naming scheme.
"""

# Code path
import os
import sys
from pathlib import Path

code_path = Path(os.getcwd())
# Files
path = code_path.joinpath('content/articles')
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))] 
files.sort(key=lambda x: x[0])
files = [os.path.join(path,f) for f in files] 
# Markdown Parser
import markdown 
md = markdown.Markdown(extensions=['meta'])

# Set Menu items
if publish:
    MENUITEMS = [(md.Meta['title'][0], f"{md.Meta['title'][0].lower().replace(' ', '-')}.html") for file in files if md.convert(Path(file).read_text(encoding='utf-8'))]
else:
    MENUITEMS = [(md.Meta['title'][0], f"/{md.Meta['title'][0].lower().replace(' ', '-')}.html") for file in files if md.convert(Path(file).read_text(encoding='utf-8'))]


HEADER_COVER = 'images/header.jpg'