# Cozy Shop

## Start project

1. Migrations

```terminaloutput
    py manage.py makemigrations
```

2. Migrate

```terminaloutput
    py manage.py migrate
```

3. When you first run a project, you need to populate the database with mock data after migration:

```terminaloutput
    py manage.py seeds
```