"""
🔐 User Registration Serializer
----------------------------------

This module defines a custom serializer for registering new users with strong
validation rules to ensure secure account creation.

Features:
- Username validation (format and uniqueness)
- Email uniqueness check (case-insensitive)
- Password strength validation (uppercase, lowercase, digit, special char)
- Secure password hashing with `set_password`
- Returns a Django `User` instance upon successful creation

Usage:
Typically used in DRF-based registration views (e.g., /api/register/).

"""

import re
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

# Regex patterns for input validation
USERNAME_REGEX = r'^[a-zA-Z0-9_]{4,30}$'  # Username: 4-30 chars, letters/digits/underscore
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'  # Password: strong security rules


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with custom field validation.

    Fields:
        - first_name: Optional
        - last_name: Optional
        - username: Required, validated with regex and uniqueness
        - email: Required, validated for uniqueness
        - password: Required, write-only, validated for strength

    Returns:
        Django User instance with hashed password
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
        }

    def validate_username(self, value):
        """
        Validates the username:
        - Must match regex pattern (4–30 characters)
        - Alphanumeric + underscore only
        - Must not already exist in the system
        """
        if not re.match(USERNAME_REGEX, value):
            raise serializers.ValidationError(
                _("Username must be 4–30 characters long and can only contain letters, digits, and underscores.")
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("This username is already taken."))

        return value

    def validate_password(self, value):
        """
        Validates password strength:
        - Minimum 8 characters
        - At least one lowercase, one uppercase, one digit, and one special character
        """
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError(
                _("Password must be at least 8 characters long and contain at least one uppercase letter, "
                  "one lowercase letter, one digit, and one special character.")
            )

        return value

    def validate_email(self, value):
        """
        Validates that the email is not already in use (case-insensitive).
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(_("This email is already registered."))
        return value

    def create(self, validated_data):
        """
        Creates and returns a new user instance after securely hashing the password.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Securely hash the password
        user.save()
        return user
