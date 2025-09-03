
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paliwalsamaj.settings')

app = Celery('paliwalsamaj')
app.conf.enable_utc = False

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Make sure celery uses Django logging
app.conf.update(worker_hijack_root_logger=False)

# Autodiscover tasks
app.autodiscover_tasks()