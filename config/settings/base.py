"""
Django Project Settings Module

This configuration file sets up all necessary settings for the Django project,
including environment loading, application registration, middleware stack,
database connection, internationalization, static/media file handling,
security configurations, REST framework settings, CORS policies,
caching, JWT authentication, and Swagger documentation options.

Key sections:

- Environment: Loads environment variables from a .env file for sensitive data.
- Base Directory: Defines the root path of the project for relative references.
- Secret Key: Fetches the Django secret key securely from environment variables.
- Installed Apps: Registers built-in Django apps, third-party packages,
  and custom applications.
- Middleware: Specifies middleware layers including security, session,
  localization, CORS, and CSRF protection.
- Security Settings: Enforces HTTPS headers and secure cookies.
- Async Task Queue: Configures Django Q cluster for asynchronous task processing.
- URL & WSGI: Specifies root URL configurations and WSGI application entrypoint.
- Templates: Defines template directories and context processors.
- Password Validators: Sets up standard Django password validation mechanisms.
- Database: Uses SQLite3 database, configured to store file in the project tmp directory.
- Localization: Sets language codes, timezone, and translation paths.
- Static & Media Files: Configures static file serving and media uploads,
  integrating WhiteNoise for static file compression.
- Default Field: Sets default primary key type for database models.
- Additional Settings: Includes simple-history revert control and URL slash handling.
- CORS Configuration: Allows frontend origins and HTTP methods for cross-origin requests.
- Caching: Configures Redis cache backend with connection details from environment.
- CSRF Trusted Origins: Specifies trusted domains for CSRF protection.
- REST Framework: Sets default authentication (JWT), permissions, filtering,
  throttling, and pagination.
- JWT Settings: Defines token lifetimes and rotation policies for security.
- Swagger: Adjusts Swagger UI compatibility mode for API docs rendering.

This modular and clear settings file is designed to support secure,
scalable, and maintainable Django applications with REST API capabilities
and frontend integration.

"""

import os
from pathlib import Path
import dotenv
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

# Load environment variables from .env file for secret keys and sensitive config
dotenv.load_dotenv()

# Define the base directory of the project for path references
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Django secret key loaded securely from environment or default fallback
SECRET_KEY = os.getenv('SECRET', 'mY1keY**')

# Installed applications: Django default, third-party and custom apps
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps for API docs, CORS, REST framework, and filtering
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'django_filters',

    # Project-specific application configuration
    'medicaldataanalysts.apps.MedicalDataAnalystsConfig',
]

# Middleware stack in order of execution, including CORS and security layers
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Enables handling of cross-origin requests

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serves static files efficiently

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Enables language selection

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection middleware

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Security settings enforcing HSTS and proxy SSL headers for HTTPS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookies security flags for session and CSRF cookies (disabled for development)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Django Q configuration for asynchronous task processing
Q_CLUSTER = {
    'name': 'DjangoORM',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}

# Root URL configuration module for request routing
ROOT_URLCONF = 'config.urls'

# Templates configuration with directories and context processors
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI application path used by deployment servers
WSGI_APPLICATION = 'config.wsgi.application'

# Password validators to enforce password security standards
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Database configuration - SQLite3 with project-relative path
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'tmp_db.sqlite3',
    }
}

# Internationalization and localization settings
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages with translations using gettext_lazy
LANGUAGES = (
    ('en', _('English')),
    ('fa', _('Farsi')),
)

# Paths where translation files are stored
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Static files configuration with WhiteNoise for efficient serving
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'staticfilesdirs'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration for user-uploaded content
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediaroot')

# Default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Disables revert functionality in django-simple-history if used
SIMPLE_HISTORY_REVERT_DISABLED = True

# Automatically append trailing slash to URLs
APPEND_SLASH = True

# Cross-Origin Resource Sharing (CORS) policies
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOW_METHODS = (
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
)
CORS_ALLOW_HEADERS = ('*',)
CORS_ALLOW_CREDENTIALS = True

# Cache configuration using Redis backend, connection via environment variable
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_LOCATION', 'redis://127.0.0.1:6379'),
        'TIMEOUT': None,
    }
}

# CSRF protection trusted origins
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
]

# Django REST Framework settings for authentication, permissions, filtering, throttling, and pagination
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/min',  # High limit for unauthenticated requests
        'user': '1000/min',  # Limit for authenticated users
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# JWT Authentication token settings using SimpleJWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Swagger/OpenAPI UI compatibility setting
SWAGGER_USE_COMPAT_RENDERERS = False
