#!/bin/sh

# wait for PSQL server to start
sleep 10

# prepare init migration
python manage.py makemigrations
# migrate db, so we have the latest db schema
python manage.py migrate
python3 manage.py loaddata AppSettings
python3 manage.py loaddata TaskTypes

# Launch celery consumer
celery worker -A pixelwalker

# Tests
python3 manage.py test engine
# start development server on public ip interface, on port 8000
python manage.py runserver 0.0.0.0:8000 