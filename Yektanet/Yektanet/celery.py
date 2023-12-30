import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Yektanet.settings")


app = Celery("Yektanet")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "calculate-hourly-stats": {
        "task": "advertiser_management.tasks.calculate_hourly_stats",
        "schedule": crontab(minute=0),
    },
    "calculate-daily-stats": {
        "task": "advertiser_management.tasks.calculate_daily_stats",
        "schedule": crontab(hour=0, minute=0),
    },
}
