#!/bin/sh

# wait for PSQL server to start
sleep 10

# prepare init migration
bash -c "python3 manage.py makemigrations"
# migrate db, so we have the latest db schema
bash -c "python3 manage.py migrate"
bash -c "python3 manage.py loaddata AppSettings"
bash -c "python3 manage.py loaddata TaskTypes"

# Launch celery consumer
bash -c "celery worker -A pixelwalker &"

# Tests
bash -c "python3 manage.py test engine"
# start development server on public ip interface, on port 8000
bash -c "python3 manage.py runserver 0.0.0.0:8000"