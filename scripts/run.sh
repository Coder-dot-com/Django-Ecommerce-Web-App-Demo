#!/bin/bash

set -e

whoami

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

gunicorn ecommerce_demo.wsgi:application --bind 0.0.0.0:8000



