# -*- coding: utf8 -*-
"""
settings.py

Configuration for Flask app

Important: Place your keys in the secret_keys.py module, 
           which should be kept out of version control.

"""

import os

from secret_keys import CSRF_SECRET_KEY, SESSION_KEY

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG_MODE = False

# Auto-set debug mode based on App Engine dev environ
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG_MODE = True

DEBUG = DEBUG_MODE

# Set secret keys for CSRF protection
SECRET_KEY = CSRF_SECRET_KEY
CSRF_SESSION_KEY = SESSION_KEY

CSRF_ENABLED = True

# Flask-DebugToolbar settings
DEBUG_TB_PROFILER_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False


# Flask-Cache settings
CACHE_TYPE = 'gaememcached'


basedir = os.path.abspath(os.path.dirname(__file__))



CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]



SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


#------------------------
# Mail server settings
#------------------------
MAIL_SERVER = 'localhost'
MAIL_PORT   = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'test'
MAIL_PASSWORD = 'test-passw'

#------------------------
# Administrator List
#------------------------
ADMINS = ['emiliano@medlista.com']


#------------------------
#------------------------
POST_PER_PAGE = 3


#------------------------
# Search
#------------------------
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50


#------------------------
#------------------------
LANGUAGES = {
    'en' : 'English',
    'es': 'Español'
}

#------------------------
# Translation
#------------------------
MS_TRANSLATOR_CLIENT_ID = '00a0794c-d4db-458d-8f5c-50e181829433'
MS_TRANSLATOR_CLIENT_SECRET= 'aKweH+XH72XvFcPPk+TEG5qbXi1XeKsBx8o2dVlE3ps='

