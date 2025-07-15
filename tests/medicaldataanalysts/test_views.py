"""
🧪 Integration Tests — medicaldataanalysts API

This test suite verifies all secured API endpoints of the `medicaldataanalysts` module.
It uses JWT authentication and covers:

- Fetching classification reports
- Getting predicted probabilities
- Viewing the processed dataset
- Training a model on demand
- Persisting model results to MongoDB
- Listing and retrieving individual saved results

Tests are powered by pytest and DRF's APIClient.
"""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from medicaldataanalysts.documents import ModelResult


@pytest.fixture
def auth_client(db):
    """
    Provides an authenticated API client with a valid JWT token.

    Creates a test user, logs them in via the login endpoint,
    and attaches the access token to client headers.

    Returns:
        APIClient: Authenticated client instance
    """
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="StrongPass123!"
    )
    client = APIClient()

    response = client.post(reverse("auth:login"), {
        "username": "testuser",
        "password": "StrongPass123!"
    })
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


def test_rf_result_endpoint(auth_client):
    """
    ✅ GET /result/rf/
    Should return a classification report containing accuracy metric.
    """
    response = auth_client.get("/api/v1/medicaldataanalysts/result/rf/")
    assert response.status_code == status.HTTP_200_OK
    assert "accuracy" in response.data


def test_y_prob_endpoint(auth_client):
    """
    ✅ GET /result/y/
    Should return class probabilities under 'y_prob'.
    """
    response = auth_client.get("/api/v1/medicaldataanalysts/result/y/")
    assert response.status_code == status.HTTP_200_OK
    assert "y_prob" in response.data


def test_data_endpoint(auth_client):
    """
    ✅ GET /data/
    Should return a list of JSON records representing cleaned dataset.
    """
    response = auth_client.get("/api/v1/medicaldataanalysts/data/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)


def test_train_model_endpoint(auth_client):
    """
    ✅ POST /train/
    Should return training results including classification report and classes.
    """
    response = auth_client.post("/api/v1/medicaldataanalysts/train/")
    assert response.status_code == status.HTTP_200_OK
    assert "rf_result" in response.data
    assert "classes" in response.data


def test_save_model_result_endpoint(auth_client):
    """
    ✅ POST /result/add/
    Should trigger training and persist result to MongoDB.
    """
    response = auth_client.post("/api/v1/medicaldataanalysts/result/add/")
    assert response.status_code == status.HTTP_201_CREATED
    assert "message" in response.data


def test_result_list_endpoint(auth_client):
    """
    ✅ GET /results/
    Should return a list of previously saved model results.
    """
    # Ensure at least one result exists
    test_save_model_result_endpoint(auth_client)

    response = auth_client.get("/api/v1/medicaldataanalysts/results/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert "id" in response.data[0]


def test_result_detail_endpoint(auth_client):
    """
    ✅ GET /results/<id>/
    Should retrieve full details of one specific result.
    """
    # Save model first
    auth_client.post("/api/v1/medicaldataanalysts/result/add/")
    obj = ModelResult.objects.first()

    response = auth_client.get(f"/api/v1/medicaldataanalysts/results/{str(obj.id)}/")
    assert response.status_code == status.HTTP_200_OK
    assert "rf_result" in response.data


def test_result_detail_not_found(auth_client):
    """
    ❌ GET /results/<invalid_id>/
    Should return 404 for a nonexistent result ID.
    """
    response = auth_client.get("/api/v1/medicaldataanalysts/results/64b000000000000000000000/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
