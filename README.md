# Cozy Shop

## Start project

### Docker

1. Create `.env` file from `.env.example` file
2. Build `docker compose up --build` containers
3. (Optional) Migrate `docker compose exec cozyshop python manage.py migrate`
4. (Optional) Make migrations `docker compose exec cozyshop python manage.py makemigrations`
5. (Optional) Load DB data `docker compose exec cozyshop python manage.py loaddata db.json`
6. (Optional) Dump DB data `docker compose exec cozyshop python manage.py dumpdata > project/db.json`
7. (Optional) Seed DB `docker compose exec cozyshop python manage.py seeds`
8. (Optional) Create Super User `docker compose exec cozyshop python manage.py createsuperuser`
9. (Optional) Stop containers `docker compose stop`
10. (Optional) Stop and remove containers `docker compose down`
11. (Optional) Start existing containers `docker compose up`
12. (Optional) Run tests `docker compose exec cozyshop coverage run --source='.' manage.py test`
13. (Optional) View tests coverage `docker compose exec cozyshop coverage ` + `report` or `html`

### OS

1. Create `env.sh` from `env.example.sh`
2. Run `source env.sh`
3. Migrate `python manage.py migrate`
4. Run Server `python manage.py runserver 0.0.0.0:8000`
5. Run Celery `celery -A config worker -E -l info` (add ` --pool=solo` for Windows)
6. Run Celery Flower `celery -A config.celery_app flower`
7. Run Celery Beat `celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`

## Checklist

1. [x] Create DB Schema ([Miro](https://miro.com/app/board/uXjVGa445i4=/?share_link_id=843826101249))
2. [x] Add all Product Page
3. [x] Add detail Product Page
4. [x] Add Filter by Category of Product
5. [x] Add Search by Name or Description of Product
6. [x] Add Authorization (forms, views, templates, email verification)
7. [x] Add Profile (model, form, views, templates)
8. [x] Add Cart functionality
9. [x] Add Order (model, form, views, templates)
10. [x] Add Payment logic (PayPal sandbox)
11. [x] Add Comment (model, form, view, template)
12. [x] Add Subscription (Celery Beat)
13. [x] Add InfoPanel (WebSocket, Celery)
14. [ ] Deploy
15. [x] Tests (Gemini)
