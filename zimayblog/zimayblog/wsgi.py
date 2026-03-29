"""
WSGI config for zimayblog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zimayblog.settings')

application = get_wsgi_application()

# NOTE: 'app' is an alias for 'application' for compatibility
# The Django app module is 'blog' (configured in INSTALLED_APPS)
app = application
