import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapper.settings')

app = Celery('scrapper')

# Load task settings from the Django settings file using the 'CELERY' namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in all installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
