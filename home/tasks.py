from celery import shared_task
import os
import requests

@shared_task
def download_image(image_url, save_directory, image_name):
  
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    image_path = os.path.join(save_directory, image_name)
    response = requests.get(image_url, stream=True)
    
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return image_path
    else:
        print(f"Failed to download image. Status Code: {response.status_code}")
        return None
    
    
from celery import shared_task
from .models import Info

@shared_task
def create_news():
    Info.objects.create(info="This is added by celery beat")
    
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

# schedule, created = IntervalSchedule.objects.get_or_create(
#     every=1,
#     period=IntervalSchedule.MINUTES
# )

schedule, created = IntervalSchedule.objects.get_or_create(
    every=3,
    period=IntervalSchedule.SECONDS
)

PeriodicTask.objects.update_or_create(
    name="Create info",
    defaults={
        'task': 'home.tasks.create_news',
        'interval': schedule,
        'args': json.dumps([]),
    }
)


