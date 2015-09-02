# -*- coding: utf-8 -*-
# Django settings for globallometree project.

import os.path
gettext = lambda s: s

PROJECT_PATH = os.path.join(os.path.dirname(__file__))
BASE_PATH = os.path.abspath(os.path.join(PROJECT_PATH, '../'))

DEBUG = True
TEMPLATE_DEBUG = True

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
MEDIA_ROOT = '/opt/globallometree_data/web/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'


TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS' : [
         os.path.join(PROJECT_PATH, 'templates'),
    ],
    'OPTIONS': {
        'context_processors':
            (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                'django.template.context_processors.csrf',
                'django.template.context_processors.request',
                "django.contrib.messages.context_processors.messages",
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                'globallometree.apps.search_helpers.context_processors.template_settings'

            )
    }
},
]


MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'globallometree.urls'

WSGI_APPLICATION = 'globallometree.wsgi.application'


CMS_TEMPLATES = (
    ('cms/basic_page.html', 'CMS basic page'),
    ('cms/home_page.html', 'CMS home page'),
)

INSTALLED_APPS = (
    # django globallometree.apps
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
    'crispy_forms',

    #django cms
    'treebeard',
    'djangocms_text_ckeditor',  # note this needs to be above the 'cms' entry
    'cms',
    'menus',
    'sekizai',
    'djangocms_link',
    'djangocms_file',
    'globallometree.plugins.linkbox',

    # project globallometree.apps
    'globallometree.apps.accounts',
    'globallometree.apps.search_helpers',
    'globallometree.apps.source',
    'globallometree.apps.data_sharing',
    'globallometree.apps.community',
    'globallometree.apps.journals',
    'globallometree.apps.taxonomy',
    'globallometree.apps.locations',
    'globallometree.apps.allometric_equations',
    'globallometree.apps.raw_data',
    'globallometree.apps.wood_densities',
    'globallometree.apps.proxy',
    'globallometree.apps.kibana_custom', #custom must go before source for overrides
    'globallometree.apps.kibana_src',
    'globallometree.apps.api',
    'globallometree.apps.biomass_expansion_factors',

    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
)


CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Override the server-derived value of SCRIPT_NAME 
# See http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers
FORCE_SCRIPT_NAME = ''

#Static files configuration
#STATIC_ROOT This is where static files get collected for serving by nginx
STATIC_ROOT = '/opt/globallometree_data/web/static/'
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
ES_URLS = ['http://localhost:9200',]
ES_INDEXES = {'default': 'globallometree'}

#Search url is the url that the browser sends requests to
#It should be the public url of the proxy server
SEARCH_URL = '/elastic'

#Celery
# CELERY_ACCEPT_CONTENT = ['json',]
# BROKER_URL = 'redis://localhost:6379/0'

# #Sessions are stored in redis so they can be shared
# #with askbot
# SESSION_ENGINE = 'redis_sessions.session'
# SESSION_REDIS_HOST = 'localhost'
# SESSION_REDIS_PORT = 6379
# SESSION_REDIS_DB = 0
# SESSION_REDIS_PREFIX = 'session'
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
        'globallometree.apps.api.renderers.BrowsableAPIRenderer',
        'globallometree.apps.api.renderers.JSONRenderer',
        'globallometree.apps.api.renderers.XMLRenderer',
        'globallometree.apps.api.renderers.CSVRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ),
    'PAGINATE_BY_PARAM' : 'limit',
    'PAGINATE_BY': 10,
    'MAX_PAGINATE_BY': 500
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
        'description': 'This is automatically generated documentation for the GlobAllomeTree API in swagger format. This page takes a few moments to load completely.',
        #'license': 'Apache 2.0',
        #'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        #'termsOfServiceUrl': 'http://globallometree.org/terms/',
        'title': 'GlobAllomeTree API Docs',
    },
}


MIGRATION_MODULES = {
    'djangocms_file': 'djangocms_file.migrations_django',
    'djangocms_flash': 'djangocms_flash.migrations_django',
    'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
    'djangocms_inherit': 'djangocms_inherit.migrations_django',
    'djangocms_link': 'djangocms_link.migrations_django',
    'djangocms_picture': 'djangocms_picture.migrations_django',
    'djangocms_snippet': 'djangocms_snippet.migrations_django',
    'djangocms_teaser': 'djangocms_teaser.migrations_django',
    'djangocms_video': 'djangocms_video.migrations_django',
    'linkbox': 'globallometree.plugins.linkbox.migrations',
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
