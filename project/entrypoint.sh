#!/bin/sh

# Apply DB migrations
echo "Applying DB migrations..."

python manage.py migrate
python manage.py makemigrations

# Apply DB seeds
echo "Applying DB seeds..."

python manage.py seeds

# Collect Static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute the provided commands or entrypoint
exec "$@"
