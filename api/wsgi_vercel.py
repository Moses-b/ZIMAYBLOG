"""
Vercel serverless entrypoint for Django.
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT_DIR / "zimayblog"

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zimayblog.settings")

app = get_wsgi_application()
