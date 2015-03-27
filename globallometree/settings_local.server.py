#This looks for the secret key if it already exists
#otherwise it writes one
def get_secret_key():
    with open('/opt/data/web/secret_key') as f:
        secret_key  = f.readlines()[0].replace('\n', '')
    return secret_key

DEBUG=False
SEARCH_URL = '/elastic/'
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
            'level': 'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/opt/globallometree_logs/error.log',
        },
      
    },
    'loggers': {
        '': {
            'handlers': ['django_log_file'],
            'level': 'ERROR',
            'propagate': True
    },
}