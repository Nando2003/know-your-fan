FROM python:3.13.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app /app
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /app

EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    mkdir -p /app/staticfiles && \
    chown -R duser:duser /app && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]