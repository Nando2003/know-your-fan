import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'know_your_fan.settings')

app = Celery('know_your_fan')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task(bind=True)
def add(x, y):
    return x + y

app.autodiscover_tasks()