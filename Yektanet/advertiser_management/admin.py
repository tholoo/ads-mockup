from django.contrib import admin
from .models import Ad, Advertiser, AdHourlyStat


@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "advertiser", "approve")
    list_display_links = ("title",)
    list_filter = ("advertiser", "approve")
    list_editable = ("approve",)
    search_fields = ("title", "advertiser__name")


@admin.register(AdHourlyStat)
class AdHourlyStatAdmin(admin.ModelAdmin):
    list_display = ("ad", "hour", "clicks", "views")
    list_display_links = ("ad",)
    list_filter = ("ad", "hour")
    search_fields = ("ad__title", "ad__advertiser__name")
