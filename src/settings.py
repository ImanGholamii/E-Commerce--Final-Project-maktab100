import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-9h2oe1air^c1*+z&v7kl%vx3)8gmg53mio7xt*zl%)-lsv!!ii'

DEBUG = True

ALLOWED_HOSTS = []

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MY_APPS = [
    'core',
    'users',
    'products',
    'orders',
    'imagess',
    'email_sender_app',

]

THIRD_PARTY_APPS = [
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    # 'rest_framework_simplejwt',
    # 'background_task',
]

INSTALLED_APPS = DJANGO_APPS + MY_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'orders.middleware.SetGuestCookieMiddleware',
    # 'orders.middleware.RedirectGuestToLoginMiddleware',
    # 'orders.middleware.MergeGuestCartMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'src.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# SETTINGS FOR PERSIAN

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
# Base URL

BASE_URL = 'http://localhost:8000'

# STATIC

STATIC_URL = 'static/'
# STATIC_ROOT = 'all_statics'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# MEDIA

MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REDIRECT URLS
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'  # home
LOGOUT_REDIRECT_URL = '/'  # home

# MY USER MODEL

AUTH_USER_MODEL = 'users.User'

# Authenticate Backends

AUTHENTICATION_BACKENDS = [
    'backends.auth.EmailOrPhoneModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# MY COOKIES

CART_COOKIE_NAME = 'shopping_cart'

# EMAIL CONFIGS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sharlotimi@gmail.com'  # Email Sender
EMAIL_HOST_PASSWORD = 'rkyb ninv cxzp xykw'  # Password App

# REST

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,
}

# Redis
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
# REDIS_DB = 1
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }
#
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
################### DEPLOY ################### 
# if DEBUG:
#     STATICFILES_DIRS = [
#         BASE_DIR / 'static'
#     ]
#
#     # Cache
#     CACHES = {
#         "default": {
#             "BACKEND": "django.core.cache.backends.dummy.DummyCache",
#         }
#     }
#
#
#     # Database
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
#
# else:
#     STATIC_ROOT = BASE_DIR / 'static'
#
#     # Cache Services:
#     # CACHES = {
#     #     "default": {
#     #         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#     #         "LOCATION": REDIS_URL,
#     #     }
#     # }
#
#
#     # Production postgresql db :
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": "fastfoodia",
#             "USER": "postgres",
#             "PASSWORD": "postgres",
#             "HOST": "localhost",
#             "PORT": 5432,
#         },
#     }
