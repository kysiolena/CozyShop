#!/bin/sh

# Apply DB migrations
echo "Applying DB migrations..."
python manage.py migrate

# Collect Static files
#echo "Collecting static files..."
#python manage.py collectstatic --noinput

# Execute the CMD from Dockerfile
exec "$@"
