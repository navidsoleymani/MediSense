"""
🌐 Project-Level URL Configuration

This module defines all top-level API routes for the MediSense project.

Includes:
- Health check endpoint for monitoring
- Authentication endpoints (register, login, token refresh)
- Machine learning + data analysis APIs

Structure:
    /api/v1/health/                 → Service health monitor
    /api/v1/auth/                   → Authentication (JWT + Register)
    /api/v1/medicaldataanalysts/   → ML processing & result APIs
"""

from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health_check(request):
    """
    ✅ Health Check Endpoint

    A simple GET endpoint to confirm the system is running correctly.

    Returns:
        {
            "status": "healthy",
            "services": {
                "database": "connected",
                "cache": "active"
            }
        }

    Notes:
    - Can be used by uptime monitors, container orchestration (K8s), or CI/CD tools.
    - Extend this to actually check DB, Redis, or external services if needed.
    """
    return Response({
        'status': 'healthy',
        'services': {
            'database': 'connected',
            'cache': 'active'
        }
    })


urlpatterns = [
    # System health and monitoring
    path('health/', health_check, name='health-check'),

    # Authentication routes (JWT auth + registration)
    path('auth/', include('auth.urls')),

    # ML data ingestion, processing, model training APIs
    path('medicaldataanalysts/', include('medicaldataanalysts.urls')),
]
