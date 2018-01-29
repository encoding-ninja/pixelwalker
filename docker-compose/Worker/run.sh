#!/bin/sh

# wait for PSQL server to start
sleep 10

# Launch celery consumer
bash -c "celery worker -A pixelwalker &"

# Tests
bash -c "python3 manage.py test worker"
