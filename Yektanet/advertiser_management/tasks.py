from datetime import timedelta

from django.utils import timezone

from celery import shared_task

from .models import Ad, AdClick, AdDailyStat, AdHourlyStat, AdView


@shared_task
def calculate_hourly_stats():
    time_threshold = timezone.now() - timedelta(hours=1)
    for ad in Ad.objects.all():
        hourly_clicks = AdClick.objects.filter(
            ad=ad, created_at__gte=time_threshold
        ).count()
        hourly_views = AdView.objects.filter(
            ad=ad, created_at__gte=time_threshold
        ).count()

        AdHourlyStat.objects.update_or_create(
            ad=ad,
            date=date,
            hour=hour,
            defaults={"clicks": hourly_clicks, "views": hourly_views},
        )


@shared_task
def calculate_daily_stats():
    time_threshold = timezone.now() - timedelta(days=1)
    for ad in Ad.objects.all():
        daily_clicks = AdClick.objects.filter(
            ad=ad, created_at__gte=time_threshold
        ).count()
        daily_views = AdView.objects.filter(
            ad=ad, created_at__gte=time_threshold
        ).count()

        AdDailyStat.objects.update_or_create(
            ad=ad,
            date=current_date,
            defaults={"total_clicks": daily_clicks, "total_views": daily_views},
        )
