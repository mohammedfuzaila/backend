#!/usr/bin/env bash
# Render build script for Django backend
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser and singleton model instances if not already present
python manage.py setup_initial_data
