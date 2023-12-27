from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView, View
from django.db.models import F

from .forms import AdForm
from .models import Ad, Advertiser


class AdvertiserView(View):
    template_name = "advertiser_management/ads.html"

    def get(self, request, *args, **kwargs):
        advertisers = Advertiser.objects.prefetch_related("ads").all()
        Advertiser.objects.all().update(views=F("views") + 1)
        Ad.objects.all().update(views=F("views") + 1)

        return render(request, self.template_name, {"advertisers": advertisers})


class AdRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs["pk"])
        ad.inc_clicks()
        return ad.link


class AdCreateView(View):
    form_class = AdForm
    template_name = "advertiser_management/ads_create.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"form": form, "error_message": "Invalid data"},
            )

        title = form.cleaned_data["title"]
        img_url = form.cleaned_data["img_url"]
        link = form.cleaned_data["link"]
        advertiser_id = form.cleaned_data["advertiser_id"]

        advertiser = get_object_or_404(Advertiser, pk=advertiser_id)
        Ad.objects.create(
            title=title, img_url=img_url, link=link, advertiser=advertiser
        )
        return HttpResponseRedirect(reverse("advertiser_management:ads"))
