import os
from django.core.exceptions import ImproperlyConfigured

# Environment Detection
# ---------------------
# Determine the current environment from DJANGO_ENV variable.
# Defaults to 'dev' (development) if not specified.
# Valid options: 'dev', 'test', 'prod' (case-insensitive)
ENV = os.getenv('DJANGO_ENV', 'dev').lower()

# Environment Validation
# ----------------------
# Ensure the specified environment is valid
if ENV not in ('dev', 'test', 'prod'):
    raise ImproperlyConfigured(
        f"Invalid DJANGO_ENV value: '{ENV}'. "
        "Must be one of: 'dev', 'test', 'prod'"
    )

# Dynamic Settings Import
# ----------------------
# Import the appropriate settings module based on environment
try:
    if ENV == 'prod':
        from .prod import *  # Production settings

        print("Loaded PRODUCTION environment settings")
    elif ENV == 'test':
        from .test import *  # Testing settings

        print("Loaded TEST environment settings")
    else:
        from .dev import *  # Development settings (default)

        print("Loaded DEVELOPMENT environment settings")

except ImportError as e:
    raise ImproperlyConfigured(
        f"Could not import settings for '{ENV}' environment: {str(e)}"
    )

# Environment Verification
# -----------------------
# Basic check to ensure required settings are loaded
if 'SECRET_KEY' not in locals():
    raise ImproperlyConfigured(
        "Settings module did not load properly - SECRET_KEY missing"
    )
