"""
📌 Authentication URL Configuration (JWT + Registration)

This module defines all authentication-related API routes, including:
- User registration
- JWT-based login and token management

Routes:
    /register/         → Create a new user account
    /login/            → Obtain access and refresh JWT tokens
    /login/refresh/    → Refresh the access token using a refresh token

Requires:
    - RegisterAPIView (custom registration view)
    - SimpleJWT views for login and token refresh

"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView

# Namespace for reverse URL lookups
app_name = 'auth'

# Authentication-related endpoints
urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),  # Custom user registration endpoint
    path('login/', TokenObtainPairView.as_view(), name='login'),  # JWT login (get access & refresh token)
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh the access token
]
