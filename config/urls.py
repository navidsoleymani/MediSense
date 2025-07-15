"""
🌐 MediSense - Root URL Configuration

This module defines the core routing structure of the MediSense platform.

Key Functionalities:
- Swagger & ReDoc API documentation endpoints (powered by drf_yasg)
- Versioned API routing for v1 endpoints
- Internationalized admin panel using i18n_patterns
- Development static & media file serving

"""

from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config.settings import (
    STATIC_URL,
    STATIC_ROOT,
    MEDIA_URL,
    MEDIA_ROOT,
)

# 📘 Swagger / OpenAPI schema view configuration
schema_view = get_schema_view(
    openapi.Info(
        title="ChronosTasker APIs",
        default_version='v1',
        description="Designed for asynchronous and periodic task execution... .",
        contact=openapi.Contact(email="navidsoleymani@ymail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# 🔗 Root-level URL patterns
urlpatterns = (
        [

            # 🔍 API schema in machine-readable formats (JSON or YAML)
            re_path(
                r'^swagger(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0),
                name='schema-json'
            ),

            # 📄 Swagger UI - interactive API documentation
            path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

            # 📘 ReDoc - alternative OpenAPI documentation
            path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

            # 📦 API v1 - routes loaded from config/interfaces/v1/
            path('api/v1/', include('config.interfaces.v1')),
        ]

        # 🛠️ Admin Panel with internationalized path support
        + i18n_patterns(
    path('admin/', admin.site.urls),
)

        # 🖼️ Static and media file handling (used in development)
        + static(STATIC_URL, document_root=STATIC_ROOT)
        + static(MEDIA_URL, document_root=MEDIA_ROOT)
)

# 🎨 Admin interface branding (i18n-compatible)
admin.site.site_header = 'MediSense'
admin.site.site_title = 'MediSense.com'
admin.site.index_title = _('MediSense Management Panel')
