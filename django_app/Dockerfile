FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./know_your_fan /know_your_fan
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /know_your_fan

EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /know_your_fan/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    chown -R duser:duser /know_your_fan && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]