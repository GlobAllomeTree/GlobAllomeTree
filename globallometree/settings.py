# -*- coding: utf-8 -*-
# Django settings for globallometree project.

import os.path
gettext = lambda s: s

PROJECT_PATH = os.path.join(os.path.dirname(__file__))
BASE_PATH = os.path.abspath(os.path.join(PROJECT_PATH, '../'))

DEBUG = True

ALLOWED_HOSTS = ('globallometree.org',
                 'www.globallometree.org',
                 'localhost',
                 'globallometree-dev.orangutaninteractive.com')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Zurich'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
#    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
#    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
    'globallometree.apps.common.context_processors.template_settings'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'globallometree.urls'

WSGI_APPLICATION = 'globallometree.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

CMS_TEMPLATES = (
    ('cms/basic_page.html', 'CMS basic page'),
    ('cms/home_page.html', 'CMS home page'),
)

INSTALLED_APPS = (
    # django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    # djangocms_admin_style must go before django.contrib.admin
    'djangocms_admin_style',  # cms
    'django.contrib.admin',
    'django.contrib.staticfiles',

    #django add ons
    'django_extensions',
    'south',
    'crispy_forms',

    'djangocms_text_ckeditor',  # note this needs to be above the 'cms' entry
    'cms',
    'menus',
    'mptt',
    'sekizai',
    'djangocms_link',
    'djangocms_file',
    'globallometree.plugins.linkbox',

    # project apps
    'globallometree.apps.common',
    'globallometree.apps.data_sharing',
    'globallometree.apps.community',
    'globallometree.apps.accounts',
    'globallometree.apps.journals',
    'globallometree.apps.data',
    'globallometree.apps.taxonomy',
    'globallometree.apps.locations',
    'globallometree.apps.search_helpers',
    'globallometree.apps.allometric_equations',
    'globallometree.apps.raw_data',
    'globallometree.apps.wood_densities',
    'globallometree.apps.kibana_custom', #custom must go before source for overrides
    'globallometree.apps.kibana_src',
    'globallometree.apps.api',
    'rest_framework',
    'rest_framework_swagger'
)


CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Override the server-derived value of SCRIPT_NAME 
# See http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers
FORCE_SCRIPT_NAME = ''

#Static files configuration
#STATIC_ROOT This is where static files get collected for serving by nginx
STATIC_ROOT = '/opt/data/web/static'
#STATIC_URL is the location the browser requests static media from
STATIC_URL = '/static/'
#STATICFILES_DIRS are static source directories
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "templates", "static"),
)


#Encoding used for export and import of data for Allometric Equations
DATA_EXPORT_ENCODING = 'cp1252'
DATA_EXPORT_ENCODING_NAME = 'Windows-1252'



#elasticutils django contrib settings
ES_URLS = ['http://127.0.01:9200',]
ES_INDEXES = {'default': 'globallometree'}

#Search url is the url that the browser sends requests to
#It should be the public url of the proxy server
SEARCH_URL = 'http://127.0.0.1:9200'

#Celery
CELERY_ACCEPT_CONTENT = ['json',]
BROKER_URL = 'redis://localhost:6379/0'

#Sessions are stored in redis so they can be shared
#with askbot
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
SESSION_REDIS_PREFIX = 'session'
SESSION_COOKIE_NAME = 'globsessionid'

DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'globallometree',      
        'USER': 'globallometree',        
        'PASSWORD': 'globallometree',                  
        'HOST': '127.0.0.1',
        'PORT': 5432, 
    },
    'askbot': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'askbot',                      # Or path to database file if using sqlite3.
        'USER': 'askbot',                      # Not used with sqlite3.
        'PASSWORD': 'askbot',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                   # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 5432,                          # Set to empty string for default. Not used with sqlite3.
    },
}

SECRET_KEY = 'KEEP_SECRET'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.XMLRenderer',
        #'rest_framework_csv.renderers.CSVRenderer', #Does not work with paginated data
        'globallometree.apps.api.renderers.SimpleBrowsableAPIRenderer',
        'globallometree.apps.api.renderers.SimpleJSONRenderer',
        'globallometree.apps.api.renderers.SimpleXMLRenderer',
        'globallometree.apps.api.renderers.SimpleCSVRenderer',
    )   
}

 
SWAGGER_SETTINGS = {
    "exclude_namespaces": [],
    "api_version": '1',
    "api_path": "/",
    "enabled_methods": [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '',
    "is_authenticated": False,
    "is_superuser": False,
    "permission_denied_handler": None,
    "info": {
        #'contact': 'apiteam@wordnik.com',
        'description': 'This is automatically generated documentation for the GlobAllomeTree API in swagger format.',
        #'license': 'Apache 2.0',
        #'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        #'termsOfServiceUrl': 'http://globallometree.org/terms/',
        'title': 'GlobAllomeTree API Docs',
    },
}


if not os.path.isfile(os.path.join(PROJECT_PATH, 'settings_local.py')):
    print "settings_local.py not present - skipping"
else:
    try:
        from settings_local import *
        print "loading settings_local.py"
    except ImportError:
        print "import error in the settings_local.py file."
        raise
