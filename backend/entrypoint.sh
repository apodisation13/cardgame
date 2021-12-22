#!/bin/bash

set -euxo pipefail

bash ./wait.sh "$POSTGRES_HOST:$POSTGRES_PORT" -- python manage.py migrate --no-input

python manage.py collectstatic --no-input

exec gunicorn config.wsgi:application -b 0.0.0.0 --reload
