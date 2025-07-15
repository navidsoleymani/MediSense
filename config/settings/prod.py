"""
Production Settings for Django Project

This configuration file is tailored for a secure and optimized
production environment with the following key features:

- DEBUG is disabled to prevent detailed error pages and sensitive
  information leakage.
- Security enhancements:
    - SECURE_SSL_REDIRECT: Forces all HTTP requests to HTTPS to
      ensure encrypted communication.
    - SECURE_CONTENT_TYPE_NOSNIFF: Adds headers to prevent
      browsers from MIME-sniffing a response away from the declared content-type.
    - SECURE_BROWSER_XSS_FILTER: Enables the browser's XSS filtering
      protection.
    - X_FRAME_OPTIONS set to 'DENY' to prevent clickjacking attacks
      by disallowing the site to be framed.
    - SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE ensure cookies
      are only sent over HTTPS.

- MongoDB connection is established via mongoengine with parameters
  loaded from environment variables for flexibility and security.
  The UUID representation is set to 'standard' for compatibility.

- REST Framework is configured to disable the Browsable API in
  production by limiting renderers to JSONRenderer only,
  enhancing security and reducing overhead.

- Cross-Origin Resource Sharing (CORS) is restricted by disabling
  allowing all origins, to enforce strict origin policies.

- Caching uses Redis backend, with the connection URI sourced from
  environment variables, supporting scalable and performant caching
  in production.

Note:
- Ensure environment variables MONGO_DB_NAME, MONGO_URI, and REDIS_LOCATION
  are properly set in the production environment.
- Properly configure SSL certificates and web server to handle HTTPS
  termination.

"""

from .base import *

import mongoengine

# Security settings for production
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# MongoDB connection configuration
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "medisense_db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017/")
mongoengine.connect(db=MONGO_DB_NAME, host=MONGO_URI, uuidRepresentation='standard')

# Disable Browsable API for security and performance
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

# Restrict CORS in production
CORS_ALLOW_ALL_ORIGINS = False

# Redis cache configuration for production
REDIS_LOCATION = os.getenv('REDIS_LOCATION', 'redis://redis:6379/1')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'TIMEOUT': None,
    }
}
