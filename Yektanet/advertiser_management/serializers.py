from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Ad, AdClick, Advertiser, AdView


class AdvertiserSerializer(serializers.ModelSerializer):
    ads = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Advertiser
        fields = ["id", "name", "ads"]


class AdSerializer(serializers.ModelSerializer):
    advertiser = serializers.PrimaryKeyRelatedField(queryset=Advertiser.objects.all())
    views_hourly = serializers.SerializerMethodField()
    clicks_hourly = serializers.SerializerMethodField()
    click_rate_hourly = serializers.SerializerMethodField()
    avg_click_time = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "img_url",
            "link",
            "advertiser",
            "approve",
            "views_hourly",
            "clicks_hourly",
            "click_rate_hourly",
            "avg_click_time",
        ]

    def get_views_hourly(self, obj):
        return obj.hourly_views

    def get_clicks_hourly(self, obj):
        return obj.hourly_clicks

    def get_click_rate_hourly(self, obj):
        return obj.hourly_click_rate

    def get_avg_click_time(self, obj):
        return obj.avg_click_time


class AdClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdClick
        fields = ["id", "ad", "ip", "created_at"]


class AdViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdView
        fields = ["id", "ad", "ip", "created_at"]
