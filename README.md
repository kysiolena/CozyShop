# Cozy Shop

## Start project

1. Move to _project_ folder `cd project/`
2. Create `.env` file from `.env.example` file in _project_ folder
3. Build `docker compose up -d --build` or start existing `docker compose up -d` containers
4. Create Super User `docker compose exec django python manage.py createsuperuser`
5. Stop containers `docker compose stop`
6. Stop and remove containers `docker compose down`

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
13. [ ] Add InfoTable (WebSocket)
14. [ ] Add Favorite
15. [ ] Tests
