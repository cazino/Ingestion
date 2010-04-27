# Django settings for mp3 project.
import mp3_localsettings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = mp3_localsettings.PROJECT_PATH # Personnal

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = mp3_localsettings.DATABASE_ENGINE   # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = mp3_localsettings.DATABASE_NAME             # Or path to database file if using sqlite3.
DATABASE_USER = mp3_localsettings.DATABASE_USER             # Not used with sqlite3.
DATABASE_PASSWORD = mp3_localsettings.DATABASE_PASSWORD         # Not used with sqlite3.
DATABASE_HOST = mp3_localsettings.DATABASE_HOST             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = mp3_localsettings.DATABASE_PORT             # Set to empty string for default. Not used with sqlite3.
DATABASE_OPTIONS = mp3_localsettings.DATABASE_OPTIONS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = mp3_localsettings.PROJECT_PATH  + '/media/'


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/mediaaaa/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'vwld*s^-3x))$_sw98*do%kk#)g3c8wfq-s@yb70j@p$c#+ogr'

INTERNAL_IPS = ('127.0.0.1',)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'mp3.urls'

TEMPLATE_DIRS = (
    PROJECT_PATH + "/main/templates",
    PROJECT_PATH + "/carousel/templates",
    PROJECT_PATH + "/highlight/templates",
    PROJECT_PATH + "/ingestion/templates",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'mp3.main',
    'mp3.carousel',
    'mp3.highlight',
    'mp3.bestsales',
    'mp3.ingestion',
    'debug_toolbar',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    #'mp3.main.context_processors.base',
)


