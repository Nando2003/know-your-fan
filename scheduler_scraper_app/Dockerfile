FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./news_scraper /news_scraper

WORKDIR /news_scraper

RUN pip install --upgrade pip && \
    pip install -r /news_scraper/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    chown -R duser:duser /news_scraper

CMD ["python", "main.py"]