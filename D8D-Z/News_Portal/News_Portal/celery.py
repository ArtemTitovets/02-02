import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

app = Celery('News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {'action_every_monday_8am':{'task': 'news.tasks.sending_emails_every_week_task',
                                                     'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
                                                     }
                         }
app.conf.timezone = 'UTC'
app.autodiscover_tasks()