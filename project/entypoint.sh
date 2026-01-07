#!/bin/sh

# Apply DB migrations
echo "Apply DB migrations"

python manage.py migrate
python manage.py makemigrations

# Apply DB seeds
echo "Apply DB seeds"

python manage.py seeds

# Execute the provided commands or entrypoint
exec "$@"
