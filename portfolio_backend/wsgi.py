"""
WSGI config for portfolio_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')

application = get_wsgi_application()

# Automatically run migrations on startup to fix Render missing table errors
try:
    from django.core.management import call_command
    print("Running automatic database migrations...")
    call_command('migrate', interactive=False)
    print("Migrations complete.")
except Exception as e:
    print(f"Error running migrations: {e}")
