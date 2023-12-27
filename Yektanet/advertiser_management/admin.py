from django.contrib import admin
from .models import Ad, Advertiser


@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ("name", "clicks", "views")
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "advertiser", "clicks", "views")
    list_display_links = ("title",)
    list_filter = ("advertiser",)
    search_fields = ("title", "advertiser__name")
