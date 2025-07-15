"""
📦 Pytest Configuration for Django (MediSense Project)

This file ensures Django is properly configured before running tests with pytest.
It sets the required environment variable for Django settings and initializes
the Django framework programmatically.

Required for:
- Django ORM support inside pytest
- Ensuring `pytest-django` knows which settings to load

Usage:
- This file will be automatically discovered by pytest
- Make sure `pytest-django` is installed in your environment

"""

import os
import django
import pytest  # Ensure pytest is available (even if unused, for IDE detection)

# Set default settings module for Django if not already defined
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize Django
django.setup()
