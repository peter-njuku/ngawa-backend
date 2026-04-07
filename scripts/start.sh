#!/bin/bash

# Exit on error
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
# Bind to 0.0.0.0 to allow external access within the container
# $PORT is provided by Render, defaulting to 8000 if not set
exec gunicorn ngawa_shop.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
