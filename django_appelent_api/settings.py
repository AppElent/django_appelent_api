"""
Django settings for django_appelent_api project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import django_heroku
import dj_database_url
import dotenv
import os
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# This is new:
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

environment = ("LOCAL" if os.getenv("ENVIRONMENT") is None else os.getenv("ENVIRONMENT")).upper()
print("Starting up environment " + environment)
if environment == 'LOCAL':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    #DEBUG_PROPAGATE_EXCEPTIONS = True

# Ignore warning about oauth scopes
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# Field encryption key
FIELD_ENCRYPTION_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if (environment == "PRODUCTION" and os.getenv('DEBUG') != '1') else True
print("Debug setting: " + str(DEBUG))

# Redirect to HTTPS on non-dev websites
if environment != "LOCAL":
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = [
    'appelent-api-dev.herokuapp.com',
    'appelent-api-staging.herokuapp.com',
    'appelent-api.herokuapp.com',
    'administratie.appelent.com',
    'localhost:3000'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'drf_yasg',
    'api.apps.ApiConfig',
    'users',
    'django_filters',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.FirebaseAuthentication',
        'api.authentication.TokenAuthSupportQueryString',
        #'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework_xml.parsers.XMLParser',
        'rest_framework_yaml.parsers.YAMLParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        'rest_framework_yaml.renderers.YAMLRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000"
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https?://([a-z0-9]+[.])*appelent[.]com",
    r"^https?://appelent-([a-z0-9]+[.])*web[.]app",
]

SWAGGER_SETTINGS = {
   #'DEFAULT_INFO': './urls.py',
}

# Setting custom user model
AUTH_USER_MODEL = 'users.User'

ROOT_URLCONF = 'django_appelent_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_appelent_api.wsgi.application'

def get_cache():
  try:
    servers = os.environ['MEMCACHIER_SERVERS']
    username = os.environ['MEMCACHIER_USERNAME']
    password = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        # TIMEOUT is not the connection timeout! It's the default expiration
        # timeout that should be applied to keys! Setting it to `None`
        # disables expiration.
        'TIMEOUT': 300,
        'LOCATION': servers,
        'OPTIONS': {
          'binary': True,
          'username': username,
          'password': password,
          'behaviors': {
            # Enable faster IO
            'no_block': True,
            'tcp_nodelay': True,
            # Keep connection alive
            'tcp_keepalive': True,
            # Timeout settings
            'connect_timeout': 2000, # ms
            'send_timeout': 750 * 1000, # us
            'receive_timeout': 750 * 1000, # us
            '_poll_timeout': 2000, # ms
            # Better failover
            'ketama': True,
            'remove_failed': 1,
            'retry_timeout': 2,
            'dead_timeout': 30,
          }
        }
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake',
#     },
#     'filesystem': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': './cache',
#         'TIMEOUT': None
#     }
# }

# configure logging
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': './debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})
logging.debug('tes123')


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())
options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)