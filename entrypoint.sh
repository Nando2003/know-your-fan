#!/bin/sh
mkdir -p /django_app/staticfiles
chown -R duser:duser /django_app

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done
echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

if [ "$1" = "celery" ]; then
  exec "$@"
fi

python manage.py test

exec "$@"