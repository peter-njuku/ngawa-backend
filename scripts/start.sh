#!/bin/bash

# Exit on error
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput 

echo "Applying database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Creating/Updating superuser if it does not exist..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if username and password:
    user, created = User.objects.get_or_create(username=username)
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
    if created:
        print(f"Superuser '{username}' created successfully.")
    else:
        print(f"Superuser '{username}' updated successfully.")
else:
    print("Superuser environment variables not set. Skipping.")
EOF

echo "Starting Gunicorn..."
# Bind to 0.0.0.0 to allow external access within the container
# $PORT is provided by Render, defaulting to 8000 if not set
exec gunicorn ngawa_shop.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
