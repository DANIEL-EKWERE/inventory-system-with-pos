#!/usr/bin/env bash
# exist on error

set -o errexit

pip install -r requirements.txt

pip install gunicorn

python manage.py collectstatic --no-input --clear

python manage.py migrate
