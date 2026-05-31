"""
WSGI config for portfolio_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')

# Automatically run migrations on startup to fix Render missing table errors
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception:
    pass

application = get_wsgi_application()
