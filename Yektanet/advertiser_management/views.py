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
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView, DetailView

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


class AdDetailView(DetailView):
    model = Ad
    template_name = "advertiser_management/ad_detail.html"
    context_object_name = "ad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = context["ad"]
        views_hourly = self.get_hourly(ad.views)
        clicks_hourly = self.get_hourly(ad.clicks)
        context["views_hourly"] = views_hourly
        context["clicks_hourly"] = clicks_hourly
        context["click_rate_all"] = ad.clicks.count() / ad.views.count()
        context["click_rate_hourly"] = [
            {"hour": view["hour"], "click_rate": click["count"] / view["count"]}
            for view, click in zip(views_hourly, clicks_hourly)
        ]

        # get the last view before each click
        last_view_before_click = (
            ad.views.filter(ip=OuterRef("ip"), created_at__lte=OuterRef("created_at"))
            .order_by("-created_at")
            .values("created_at")[:1]
        )

        annotated_clicks = ad.clicks.annotate(
            last_view_time=Subquery(last_view_before_click)
        )

        # get the delta time between the click and the view before it in seconds
        aggregated = annotated_clicks.aggregate(
            avg_click_time=Avg(
                ExpressionWrapper(
                    F("created_at") - F("last_view_time"),
                    output_field=fields.DurationField(),
                )
            )
        )

        context["avg_click_time"] = (
            aggregated["avg_click_time"].total_seconds()
            if aggregated["avg_click_time"]
            else 0
        )
        return context

    def get_hourly(self, objects):
        return (
            objects.annotate(hour=ExtractHour("created_at"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        )
