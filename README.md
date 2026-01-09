# Cozy Shop

## Start project

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
12. [ ] Add Subscription (Celery)
13. [x] Add InfoPanel (WebSocket, Celery)
14. [ ] Deploy
15. [ ] Tests
