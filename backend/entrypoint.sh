#!/bin/bash

set -euxo pipefail

bash ./wait.sh "$POSTGRES_HOST:$POSTGRES_PORT" -- python manage.py migrate --no-input

bash ls -a

python manage.py collectstatic

exec gunicorn config.wsgi:application -b 0.0.0.0 --reload
