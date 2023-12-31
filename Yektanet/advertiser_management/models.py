from django.db import models, transaction
from django.db.models import (
    F,
    Count,
    Avg,
    OuterRef,
    Subquery,
    ExpressionWrapper,
    fields,
)
from django.db.models.functions import ExtractHour


class Advertiser(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"({self.id}) {self.name}"


class Ad(models.Model):
    title = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    advertiser = models.ForeignKey(
        Advertiser, related_name="ads", on_delete=models.CASCADE
    )
    approve = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.id}) {self.title} - {self.advertiser.name}"

    def get_hourly_stats(self, queryset):
        return (
            queryset.annotate(hour=ExtractHour("created_at"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        )

    @property
    def hourly_views(self):
        return self.get_hourly_stats(self.views)

    @property
    def hourly_clicks(self):
        return self.get_hourly_stats(self.clicks)

    @property
    def click_rate(self):
        return self.clicks.count() / self.views.count()

    @property
    def hourly_click_rate(self):
        views_hourly = self.hourly_views
        clicks_hourly = self.hourly_clicks
        return [
            {"hour": view["hour"], "click_rate": click["count"] / view["count"]}
            for view, click in zip(views_hourly, clicks_hourly)
        ]

    @property
    def avg_click_time(self):
        last_view_before_click = (
            self.views.filter(ip=OuterRef("ip"), created_at__lte=OuterRef("created_at"))
            .order_by("-created_at")
            .values("created_at")[:1]
        )
        annotated_clicks = self.clicks.annotate(
            last_view_time=Subquery(last_view_before_click)
        )
        aggregated = annotated_clicks.aggregate(
            avg_click_time=Avg(
                ExpressionWrapper(
                    F("created_at") - F("last_view_time"),
                    output_field=fields.DurationField(),
                )
            )
        )
        return (
            aggregated["avg_click_time"].total_seconds()
            if aggregated["avg_click_time"]
            else 0
        )


class AdClick(models.Model):
    ad = models.ForeignKey(
        "advertiser_management.Ad", related_name="clicks", on_delete=models.CASCADE
    )
    ip = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.id}) {self.ad.title}"


class AdView(models.Model):
    ad = models.ForeignKey(
        "advertiser_management.Ad", related_name="views", on_delete=models.CASCADE
    )
    ip = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.id}) {self.ad.title}"
