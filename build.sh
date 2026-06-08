#!/usr/bin/env bash
# Render build script for Django backend
set -o errexit

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Running database migrations ==="
python manage.py migrate --verbosity 2

echo "=== Setting up initial data ==="
# Create superuser and singleton model instances if not already present
python manage.py setup_initial_data

echo "=== Seeding database with fallback data ==="
python seed_db.py

echo "=== Build complete! ==="
