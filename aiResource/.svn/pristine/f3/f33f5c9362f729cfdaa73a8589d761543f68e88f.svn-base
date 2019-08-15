#!/usr/bin/env bash
nohup python manage.py  celery worker -B -l info &
nohup python manage.py celery worker -c 4 --loglevel=info &