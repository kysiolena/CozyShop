# Cozy Shop

## Start project

1. Create `env.sh` file from `env.example.sh` file
2. Set environment variables by command `source env.sh`
3. Migrations

    ```terminaloutput
        py manage.py makemigrations
    ```
4. Migrate

    ```terminaloutput
        py manage.py migrate
    ```

5. When you first run a project, you need to populate the database with mock data after migration:

    ```terminaloutput
        py manage.py seeds
    ```

6. Create Super User

    ```terminaloutput
        py manage.py createsuperuser
    ```

## Checklist

1. [ ] Create DB
   Schema ([DB Diagram Builder](https://www.figma.com/community/file/1077327065994144868/database-diagram-builder))
2. [x] Add all Product Page
3. [x] Add detail Product Page
4. [x] Add Filter by Category of Product
5. [ ] Add Search by Name or Description of Product
6. [ ] Add Authorization (forms, views, templates, email verification)
7. [ ] Add Profile (model, form, views, templates)
8. [ ] Add Cart functionality
9. [ ] Add Order (model, form, views, templates)
10. [ ] Add Payment logic (PayPal sandbox)
11. [ ] Add Comment (model, form, view, template)
12. [ ] Add Subscription (Celery)
13. [ ] Add InfoTable (WebSocket)
14. [ ] Add Favorite
15. [ ] Tests
