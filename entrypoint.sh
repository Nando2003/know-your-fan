#!/bin/sh
set -e

# 1) Garante pasta de estáticos (no named volume)
# mkdir -p /django_app/staticfiles

# 2) Espera Postgres estar pronto
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 2
done

# 3) Celery vs Web
if [ "$RUN_MODE" = "celery" ]; then
  exec celery --app=core.celery:app worker --loglevel=INFO
fi

# 4) Coleta estáticos, migrações e testes
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py test

# 5) Uvicorn
if [ "$DEBUG" = "1" ]; then
  echo "DEBUG MODE 🤖"
  exec python manage.py runserver 0.0.0:8000
else
  exec uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --workers 4
fi
