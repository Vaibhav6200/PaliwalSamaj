#!/bin/sh
set -e

if [ "$DB_HOST" = "db" ]; then
  echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 1
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
