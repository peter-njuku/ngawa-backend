#!/bin/bash

# Exit on error
set -e

echo "Applying database migrations..."
python manage.py migrate

echo "Initializing admin user..."
python manage.py init_admin

echo "Seeding default categories..."
python manage.py seed_categories

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 ngawasolutions.wsgi:application
