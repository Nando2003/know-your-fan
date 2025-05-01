#!/bin/sh
mkdir -p /django_app/staticfiles
chown -R duser:duser /django_app

echo "Me ajuda senhor, eu não sei o que fazer"
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done
echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver 0.0.0.0:8000

exec uvicorn know_your_fan:asgi:application --reload --host 0.0.0.0 --port 8000 --workers 4