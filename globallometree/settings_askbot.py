import os.path
import logging
import sys
import askbot
import site

# TODO: already defined in the main settings module
PROJECT_PATH = os.path.join(os.path.dirname(__file__))
BASE_PATH = os.path.abspath(os.path.join(PROJECT_PATH, '../'))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_PATH, 'static_collected')

#this line is added so that we can import pre-packaged askbot dependencies
ASKBOT_ROOT = os.path.abspath(os.path.dirname(askbot.__file__))
site.addsitedir(os.path.join(ASKBOT_ROOT, 'deps'))

PROJECT_ROOT = os.path.dirname(__file__)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'#must be this value

JINJA2_EXTENSIONS = (
    'compressor.contrib.jinja2ext.CompressorExtension',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

#UPLOAD SETTINGS
FILE_UPLOAD_TEMP_DIR = os.path.join(
                                os.path.dirname(__file__),
                                'tmp'
                            ).replace('\\','/')

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

ASKBOT_ALLOWED_UPLOAD_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ASKBOT_MAX_UPLOAD_FILE_SIZE = 1024 * 1024 #result in bytes

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

#TEMPLATE_DIRS = (,) #template have no effect in askbot, use the variable below
#ASKBOT_EXTRA_SKINS_DIR = #path to your private skin collection
#take a look here http://askbot.org/en/question/207/

#setup memcached for production use!
#see http://docs.djangoproject.com/en/1.1/topics/cache/ for details
#CACHE_BACKEND = 'locmem://'
#needed for django-keyedcache
#CACHE_TIMEOUT = 6000
#sets a special timeout for livesettings if you want to make them different
#LIVESETTINGS_CACHE_TIMEOUT = CACHE_TIMEOUT
#CACHE_PREFIX = 'askbot' #make this unique
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
#If you use memcache you may want to uncomment the following line to enable memcached based sessions
#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'askbot.deps.django_authopenid.backends.AuthBackend',
)

#logging settings
# LOG_FILENAME = 'askbot.log'
# logging.basicConfig(
#     filename=os.path.join(os.path.dirname(__file__), 'log', LOG_FILENAME),
#     level=logging.CRITICAL,
#     format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
# )

###########################
#
#   this will allow running your forum with url like http://site.com/forum
#
#   ASKBOT_URL = 'forum/'
#
ASKBOT_URL = 'forum/' #no leading slash, default = '' empty string
ASKBOT_TRANSLATE_URL = True #translate specific URLs
_ = lambda v:v #fake translation function for the login url
LOGIN_URL = '/%s%s%s' % (ASKBOT_URL,_('account/'),_('signin/'))
LOGIN_REDIRECT_URL = ASKBOT_URL #adjust if needed
#note - it is important that upload dir url is NOT translated!!!
#also, this url must not have the leading slash
ALLOW_UNICODE_SLUGS = False
ASKBOT_USE_STACKEXCHANGE_URLS = False #mimic url scheme of stackexchange

#Celery Settings
BROKER_TRANSPORT = "djkombu.transport.DatabaseTransport"
CELERY_ALWAYS_EAGER = True

import djcelery
djcelery.setup_loader()

CSRF_COOKIE_NAME = 'askbot_csrf'
#enter domain name here - e.g. example.com
CSRF_COOKIE_DOMAIN = 'globallometree.org'

STATICFILES_DIRS = (
    ('default/media', os.path.join(ASKBOT_ROOT, 'media')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

RECAPTCHA_USE_SSL = True

#HAYSTACK_SETTINGS
ENABLE_HAYSTACK_SEARCH = False
#Uncomment for multilingual setup:
#HAYSTACK_ROUTERS = ['askbot.search.haystack.routers.LanguageRouter',]

#Uncomment if you use haystack
#More info in http://django-haystack.readthedocs.org/en/latest/settings.html
#HAYSTACK_CONNECTIONS = {
#            'default': {
#                        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#            }
#}

TINYMCE_COMPRESSOR = True
TINYMCE_SPELLCHECKER = False
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'default/media/js/tinymce/')

#TINYMCE_JS_URL = STATIC_URL + 'default/media/js/tinymce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'askbot_imageuploader,askbot_attachment',
    'convert_urls': False,
    'theme': 'advanced',
    'force_br_newlines': True,
    'force_p_newlines': False,
    'forced_root_block': '',
    'mode' : 'textareas',
    'oninit': "TinyMCE.onInitHook",
    'plugins': 'askbot_imageuploader,askbot_attachment',
    'theme_advanced_toolbar_location' : 'top',
    'theme_advanced_toolbar_align': 'left',
    'theme_advanced_buttons1': 'bold,italic,underline,|,bullist,numlist,|,undo,redo,|,link,unlink,askbot_imageuploader,askbot_attachment',
    'theme_advanced_buttons2': '',
    'theme_advanced_buttons3' : '',
    'theme_advanced_path': False,
    'theme_advanced_resizing': True,
    'theme_advanced_resize_horizontal': False,
    'theme_advanced_statusbar_location': 'bottom',
    'width': '730',
    'height': '250'
}

#delayed notifications, time in seconds, 15 mins by default
NOTIFICATION_DELAY_TIME = 60 * 15

GROUP_MESSAGING = {
    'BASE_URL_GETTER_FUNCTION': 'askbot.models.user_get_profile_url',
    'BASE_URL_PARAMS': {'section': 'messages', 'sort': 'inbox'}
}

ASKBOT_MULTILINGUAL = False

ASKBOT_CSS_DEVEL = False
if 'ASKBOT_CSS_DEVEL' in locals() and ASKBOT_CSS_DEVEL == True:
    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc {infile} {outfile}'),
    )

COMPRESS_JS_FILTERS = []
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
JINJA2_EXTENSIONS = ('compressor.contrib.jinja2ext.CompressorExtension',)

# Use syncdb for tests instead of South migrations. Without this, some tests
# fail spuriously in MySQL.
SOUTH_TESTS_MIGRATE = False

VERIFIER_EXPIRE_DAYS = 3
ASKBOT_SELF_TEST = False
