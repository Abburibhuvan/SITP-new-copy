#!/bin/bash

echo "Starting deployment setup..."

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run automatic setup
echo "Running automatic setup..."
python auto_setup.py

# Start gunicorn
echo "Starting Gunicorn server..."
exec gunicorn TAU.wsgi:application --bind 0.0.0.0:8080 --log-file - --access-logfile - --workers 2
