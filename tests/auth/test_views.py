"""
✅ Integration Test Suite — Authentication APIs

This module validates the functionality of the authentication system in MediSense,
including registration and JWT login endpoints. It uses Pytest and DRF's APIClient.

Tests Covered:
- User registration (success, existing username, weak password)
- JWT login (token generation)
- Token refresh using valid refresh token

"""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def client():
    """
    Provides a reusable API client for making HTTP requests in tests.
    """
    return APIClient()


@pytest.mark.django_db
def test_register_user_success(client):
    """
    ✅ Should successfully register a user with valid data.
    """
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe_123",
        "email": "john@example.com",
        "password": "StrongPass123!"
    }
    url = reverse("auth:register")
    response = client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "username" in response.data
    assert response.data["username"] == payload["username"]


@pytest.mark.django_db
def test_register_existing_username(client, django_user_model):
    """
    🔁 Should return 400 if the username is already taken.
    """
    django_user_model.objects.create_user(username="duplicate", password="Test123!!")

    payload = {
        "first_name": "Ali",
        "last_name": "Soleymani",
        "username": "duplicate",
        "email": "ali@example.com",
        "password": "AnotherPass456!"
    }
    url = reverse("auth:register")
    response = client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_register_invalid_password(client):
    """
    🚫 Should reject weak password during registration.
    """
    payload = {
        "first_name": "Lara",
        "last_name": "Croft",
        "username": "lara_croft",
        "email": "lara@example.com",
        "password": "weakpass"
    }
    url = reverse("auth:register")
    response = client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data


@pytest.mark.django_db
def test_jwt_login_success(client, django_user_model):
    """
    🔐 Should issue access and refresh tokens for valid credentials.
    """
    django_user_model.objects.create_user(
        username="testjwtuser", password="TestJWTpass123!"
    )

    payload = {"username": "testjwtuser", "password": "TestJWTpass123!"}
    url = reverse("auth:login")
    response = client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_jwt_refresh_token(client, django_user_model):
    """
    🔄 Should return a new access token using refresh token.
    """
    django_user_model.objects.create_user(
        username="refreshuser", password="TestRefresh123!"
    )

    login_payload = {"username": "refreshuser", "password": "TestRefresh123!"}
    login_response = client.post(reverse("auth:login"), login_payload, format="json")

    refresh_token = login_response.data["refresh"]
    refresh_response = client.post(reverse("auth:token_refresh"), {"refresh": refresh_token}, format="json")

    assert refresh_response.status_code == status.HTTP_200_OK
    assert "access" in refresh_response.data
