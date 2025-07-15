"""
Django Settings Validator

This module provides a function to validate critical Django settings
based on the environment. It ensures that the settings meet security 
standards for both production and development environments. The 
validator raises exceptions for production violations and issues 
warnings for potential misconfigurations in development.

Key Validation Rules:
1. SECRET_KEY: For production environments, the SECRET_KEY must 
   be set to a strong, non-default value. If the key is missing or 
   set to the default value 'mY1keY**', an ImproperlyConfigured 
   exception is raised.
2. ALLOWED_HOSTS: In development, a wildcard '*' is allowed for 
   ALLOWED_HOSTS, but a warning is raised if DEBUG is enabled with 
   an insecure ALLOWED_HOSTS setting. In production, this should 
   be restricted to trusted domains.

Usage:
- Simply call the `validate_settings(settings)` function within 
  your Django settings or startup process.
  
Arguments:
    settings: The Django settings module object, typically 
              imported as `from django.conf import settings`.

Exceptions:
    ImproperlyConfigured: Raised if a critical setting is 
                           misconfigured in production.
    RuntimeWarning: Issued when a potential issue is detected 
                    in the development environment.

Example:
    validate_settings(settings)
    
Author: Your Project Team
"""

from django.core.exceptions import ImproperlyConfigured

def validate_settings(settings):
    """
    Validate critical Django settings with environment-specific rules.
    
    This validator enforces production security standards while allowing
    development flexibility with appropriate warnings.
    
    Args:
        settings: Django settings module object
        
    Raises:
        ImproperlyConfigured: For production environment violations
        RuntimeWarning: For development environment security warnings
    """
    
    # Production SECRET_KEY validation
    # Enforces that production must have a properly configured secret key
    if not settings.DEBUG and (not settings.SECRET_KEY or settings.SECRET_KEY == 'mY1keY**'):
        raise ImproperlyConfigured(
            "SECRET_KEY must be properly configured in production! "
            "Please set a strong secret key in environment variables."
        )
    
    # Development ALLOWED_HOSTS warning
    # Warns about permissive hosts in development without blocking execution
    if settings.DEBUG and settings.ALLOWED_HOSTS == ['*']:
        import warnings
        warnings.warn(
            "DEBUG mode with wildcard ALLOWED_HOSTS is insecure! "
            "For development only, restrict in production.",
            RuntimeWarning
        )
