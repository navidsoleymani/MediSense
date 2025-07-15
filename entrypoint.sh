#!/bin/bash

# ┌──────────────────────────────────────────────┐
# │         🚀 Django Application Entrypoint     │
# └──────────────────────────────────────────────┘
#
# This script is used as the container entrypoint
# for launching the Django backend via Gunicorn.
#
# - Gunicorn: WSGI HTTP server for UNIX
# - Gevent: Asynchronous worker class for handling concurrent requests
# - Timeout: 120 seconds for long-running ML tasks or slow APIs
# - Binding: Listens on 0.0.0.0:8000 inside container
#
# Recommended use: production-ready containers with Gunicorn
# ------------------------------------------------------------------

echo "🔧 Starting Django server with Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --worker-class gevent
