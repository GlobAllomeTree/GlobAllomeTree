#This looks for the secret key if it already exists
#otherwise it writes one
def get_secret_key():
    with open('/opt/data/web/secret_key') as f:
        secret_key  = f.readlines()[0].replace('\n', '')
    return secret_key

DEBUG=True

#This should coincide with the configuration in nginx that points to 
#the elasticsearch proxy
SEARCH_URL = '/search/'

SECRET_KEY = get_secret_key()
LOGGING = {
'version': 1,
    'disable_existing_loggers': False,
    'filters': {
       'require_debug_false_filter': {
            '()': 'django.utils.log.RequireDebugFalse'
          }
    },
    'handlers': {
        'django_log_file': {
            'level': 'WARNING',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/opt/logs/web/django.log',
        },
        # The mail_adminds handler is taken from the default django
        # logging configuration
        # This handler will take any records of ERROR level and send them 
        # user the AdminEmailHandler
        # It filters to make sure DEBUG is False and the log handler is only 
        # included in the django.request logger below
        'mail_admins_handler': {
            'level': 'ERROR',
            'filters': ['require_debug_false_filter'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['django_log_file'],
            'level': 'WARNING',
            'propagate': True,
        },
        # 'django.request' is a logger special for errors that are 
        # seen by end users, since django.request handles user requests
        # This config block basically says:
        # Any messages with level ERROR and above
        # that happen in the 'django.request' module
        # will be handled by the 'mail_admins_handler'
        # and WILL be propogated further to other loggers 
        # that are less specific, for example the root logger
        'django.request': {
            'handlers': ['mail_admins_handler'],
            'level': 'ERROR',
            'propagate': True
        }, 
    },
}