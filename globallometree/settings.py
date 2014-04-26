# -*- coding: utf-8 -*-
# Django settings for globallometree project.

import os.path

gettext = lambda s: s

PROJECT_PATH = os.path.join(os.path.dirname(__file__))
BASE_PATH = os.path.abspath(os.path.join(PROJECT_PATH, '../'))

ALLOWED_HOSTS = []

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

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
USE_I18N = True # TODO: check if this can be False

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

    #below is askbot stuff for this tuple
    #'askbot.skins.loaders.load_template_source', #changed due to bug 97
    'askbot.skins.loaders.filesystem_load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',

    #askbot
    'askbot.context.application_settings',
    'askbot.user_messages.context_processors.user_messages',#must be before auth
    'django.core.context_processors.csrf', #necessary for csrf protection
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
    #below is askbot stuff for this tuple
    'askbot.middleware.anon_user.ConnectToSessionMessagesMiddleware',
    'askbot.middleware.forum_mode.ForumModeMiddleware',
    'askbot.middleware.cancel.CancelActionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'askbot.middleware.view_log.ViewLogMiddleware',
    'askbot.middleware.spaceless.SpacelessMiddleware',
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

    #Search related apps
    'haystack',
    'elasticstack',

    # Django CMS apps
    'djangocms_text_ckeditor',  # note this needs to be above the 'cms' entry
    'cms',
    'menus',
    'mptt',
    'sekizai',
    'djangocms_link',
    'djangocms_file',

    # project apps
    'globallometree.apps.common',
    'globallometree.apps.accounts',
    'globallometree.apps.journals',
    'globallometree.apps.data',
    'globallometree.apps.taxonomy',
    'globallometree.apps.locations',
    'globallometree.apps.allometric_equations',
    'globallometree.apps.wood_densities',
    'globallometree.apps.bootstrap_3_theme', #our app must got first here for overrides
    'bootstrap3', 

    # 'globallometree.apps.original_theme',
    'globallometree.apps.kibana_custom', #custom must go before source for overrides
    'globallometree.apps.kibana_src',
    'globallometree.plugins.linkbox',

    # askbot
    'longerusername',
    #all of these are needed for the askbot
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'compressor',
    #'debug_toolbar',
    'askbot',
    #'askbot.deps.django_authopenid',
    #'askbot.importers.stackexchange', #se loader
    'askbot.deps.livesettings',
    'keyedcache',
    'robots',
    'django_countries',
    'djcelery',
    'djkombu',
    'followit',
    'tinymce',
    #'avatar',#experimental use git clone git://github.com/ericflo/django-avatar.git$
    'compressor',
    'group_messaging',
)


CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Override the server-derived value of SCRIPT_NAME 
# See http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers
FORCE_SCRIPT_NAME = ''

#Static files configuration
STATIC_ROOT = os.path.join(BASE_PATH, 'static_collected')
STATIC_URL = '/static/'


#Encoding used for export and import of data
DATA_EXPORT_ENCODING = 'cp1252'
DATA_EXPORT_ENCODING_NAME = 'Windows-1252'


from settings_search import *
from settings_local import *
from settings_askbot import *