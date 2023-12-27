from django.db import models
from django.db.models import F


class Advertiser(models.Model):
    name = models.CharField(max_length=200)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"({self.id}) {self.name}"


class Ad(models.Model):
    title = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    advertiser = models.ForeignKey(
        Advertiser, related_name="ads", on_delete=models.CASCADE
    )
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"({self.id}) {self.title} - {self.advertiser.name}"

    def inc_clicks(self):
        Ad.objects.filter(pk=self.pk).update(clicks=F("clicks") + 1)
        self.advertiser.clicks = F("clicks") + 1
        self.advertiser.save()
