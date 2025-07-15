"""
Development Settings Module for Django Project

This configuration file extends the base settings specifically for
development purposes. It includes debugging options, local MongoDB
connection setup via MongoEngine, development-specific MongoDB options,
REST framework renderer adjustments, and relaxed CORS and cache settings.

Key features:

- Debug Mode: Enabled to provide detailed error pages and auto-reload.
- Allowed Hosts: Configured to accept requests from all hosts during development.
- Internal IPs: Set to localhost for debugging tools like Django Debug Toolbar.
- MongoDB Connection: Uses environment variables to connect to a MongoDB instance
  with MongoEngine, specifying database name and URI with standard UUID representation.
- MongoDB Dev Settings: Enables automatic index creation and query debugging for development ease.
- REST Framework Renderers: Adds BrowsableAPIRenderer to enable interactive API exploration in development.
- CORS: Allows all origins for cross-origin resource sharing, facilitating frontend development.
- Cache Backend: Uses local in-memory cache suitable for development without external dependencies.

This setup aims to create a flexible, developer-friendly environment
with helpful debugging tools and easy local MongoDB integration,
while minimizing external dependencies.

"""

from .base import *

import os
import mongoengine

# Enable debug mode for detailed error reporting and hot reload during development
DEBUG = True

# Allow all hosts for ease of local and network testing
ALLOWED_HOSTS = ['*']

# Define internal IPs for debugging tools such as Django Debug Toolbar
INTERNAL_IPS = ['127.0.0.1']

# MongoDB connection configuration using environment variables or defaults
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "medisense_db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017/")

# Connect to MongoDB using MongoEngine with standard UUID representation
mongoengine.connect(db=MONGO_DB_NAME, host=MONGO_URI, uuidRepresentation='standard')

# Development-specific MongoDB settings
MONGO_DEV_SETTINGS = {
    'AUTO_INDEX': True,  # Automatically create indexes for models
    'DEBUG_QUERIES': True  # Enable logging of all queries to help debugging
}

# Extend REST framework to include Browsable API renderer for interactive API browsing
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]

# Enable CORS for all origins to facilitate frontend development and testing
CORS_ALLOW_ALL_ORIGINS = True

# Use in-memory cache backend suitable for local development environment
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
