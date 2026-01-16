pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate --noinput

python manage.py seeds

python manage.py create_admin_user