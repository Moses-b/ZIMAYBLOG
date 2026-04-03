"""
WSGI config for app.

This module exposes the WSGI application for the app.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zimayblog.settings')

# This is needed for Gunicorn to find the app
app = get_wsgi_application()