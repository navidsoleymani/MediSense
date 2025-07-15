from django.conf import settings
from .settings.validators import validate_settings

validate_settings(settings)
