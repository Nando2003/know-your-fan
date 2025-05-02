FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./django_app /django_app
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /django_app

EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /django_app/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    chown -R duser:duser /django_app && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]