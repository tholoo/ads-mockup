from django.db import models, transaction
from django.db.models import F


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

    def __str__(self):
        return f"({self.id}) {self.title} - {self.advertiser.name}"


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
