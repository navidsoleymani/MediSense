"""
Test Configuration for Django Project

This configuration is optimized for running Django's test suite.
It includes settings designed to ensure a smooth testing experience
while using MongoDB and Django REST Framework. Key features:

- DEBUG is enabled to provide detailed error messages during testing.
- The test runner is set to DiscoverRunner, which is the default
  test runner in Django for discovering and running tests.

MongoDB Connection:
- MongoDB is configured through mongoengine, using environment
  variables to load the database name and URI. This ensures
  flexibility and allows tests to run against different databases
  based on environment settings.

Test Optimizations:
- Caching is disabled by using DummyCache to avoid unnecessary
  cache interactions during tests.
- The default password hasher is set to MD5PasswordHasher to speed up
  test execution by using a fast but insecure password hashing method.
  This is only for testing purposes and should never be used in production.

Rate Limiting Adjustments:
- DRF throttling is reduced or disabled during tests to avoid running
  into rate-limiting issues and ensure smooth execution of API tests.

Note:
- Ensure that environment variables MONGO_DB_NAME and MONGO_URI are
  set properly for the test environment.
- This configuration should be used exclusively for testing and never
  in production environments.

"""

from .base import *

import mongoengine

# Test Configuration for the Django test suite
DEBUG = True
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# MongoDB connection configuration for testing
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "medisense_db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017/")
mongoengine.connect(db=MONGO_DB_NAME, host=MONGO_URI, uuidRepresentation='standard')

# Test optimizations
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Use fast MD5 hashing for password validation in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable DRF throttling during tests to avoid rate-limiting issues
REST_FRAMEWORK.update({
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {}
})
