from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    RedirectView,
    TemplateView,
)

from .models import Ad, AdClick, Advertiser, AdView


class AdvertiserView(TemplateView):
    template_name = "advertiser_management/ads.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        advertisers = Advertiser.objects.prefetch_related("ads").all()

        # add a view for each ad
        ip = self.request.META.get("REMOTE_ADDR")
        AdView.objects.bulk_create([AdView(ad=ad, ip=ip) for ad in Ad.objects.all()])

        context["advertisers"] = advertisers
        return context


class AdRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs["pk"])

        # record a click for the ad
        ip = self.request.META.get("REMOTE_ADDR")
        AdClick.objects.create(ad=ad, ip=ip)

        return ad.link


class AdCreateView(CreateView):
    model = Ad
    fields = ["advertiser", "img_url", "title", "link"]
    labels = {
        "img_url": "Image",
        "link": "URL",
    }
    template_name = "advertiser_management/ads_create.html"
    success_url = reverse_lazy("advertiser_management:ads")


class AdDetailView(DetailView):
    model = Ad
    template_name = "advertiser_management/ad_detail.html"
    context_object_name = "ad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = context["ad"]
        context["views_hourly"] = ad.hourly_views
        context["clicks_hourly"] = ad.hourly_clicks
        context["click_rate_all"] = ad.click_rate
        context["click_rate_hourly"] = ad.hourly_click_rate
        context["avg_click_time"] = ad.avg_click_time
        return context
