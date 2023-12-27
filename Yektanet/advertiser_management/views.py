from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView

from .forms import AdForm
from .models import Ad, Advertiser, AdClick, AdView


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


class AdCreateView(FormView):
    form_class = AdForm
    template_name = "advertiser_management/ads_create.html"
    success_url = reverse_lazy("advertiser_management:ads")

    def form_valid(self, form):
        title = form.cleaned_data["title"]
        img_url = form.cleaned_data["img_url"]
        link = form.cleaned_data["link"]
        advertiser_id = form.cleaned_data["advertiser_id"]

        advertiser = get_object_or_404(Advertiser, pk=advertiser_id)
        Ad.objects.create(
            title=title, img_url=img_url, link=link, advertiser=advertiser
        )
        return super().form_valid(form)
