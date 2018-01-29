#!/bin/sh

# wait for PSQL server to start
sleep 10

# Launch celery consumer
celery worker -A pixelwalker

# Tests
python3 manage.py test worker
