import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paliwalsamaj.settings')

app = Celery('paliwalsamaj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
