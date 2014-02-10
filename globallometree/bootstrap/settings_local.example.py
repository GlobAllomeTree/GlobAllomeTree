

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


#These people get error logs
ADMINS = (
     ('Admin Name', 'example@gmail.com'),
)

#These people get notices of new users... data submissions, etc...
MANAGERS = (
     ('Manager Name', 'example@gmail.com'),
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = ''