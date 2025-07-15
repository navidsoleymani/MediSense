"""
🧾 User Registration API View

This module defines a public API endpoint for registering new users.
It leverages Django REST Framework's generic `CreateAPIView` to handle
the POST request, using a custom `RegisterSerializer` for validation.

Features:
- Accepts: first_name, last_name, username, email, password
- Validates input via RegisterSerializer (regex, uniqueness, strength)
- Allows unauthenticated access (for open signup)
- Returns a 201 response on successful registration

Endpoint:
    POST /api/auth/register/
"""

from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterAPIView(CreateAPIView):
    """
    Public API endpoint to register new users.

    Inherits:
        - DRF's CreateAPIView to handle POST requests.

    Permissions:
        - AllowAny: No authentication required to register.

    Serializer:
        - RegisterSerializer handles all validation and user creation.

    Returns:
        - 201 Created with User info (excluding password)
        - 400 Bad Request if validation fails
    """
    permission_classes = [AllowAny]           # Open to unauthenticated users
    serializer_class = RegisterSerializer     # Handles validation and user creation
    queryset = User.objects.all()             # Required by CreateAPIView (not directly used here)
