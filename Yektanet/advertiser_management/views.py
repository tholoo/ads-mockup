from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Ad, AdClick, Advertiser, AdView
from .serializers import AdSerializer, AdvertiserSerializer


class AdvertiserViewSet(ModelViewSet):
    queryset = Advertiser.objects.prefetch_related("ads").all()
    serializer_class = AdvertiserSerializer

    def list(self, request, *args, **kwargs):
        # add a view for each ad
        ip = request.META.get("REMOTE_ADDR")
        AdView.objects.bulk_create([AdView(ad=ad, ip=ip) for ad in Ad.objects.all()])

        return super().list(request, *args, **kwargs)


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    # redirect on /ads/<pk>/click/
    @action(detail=True, methods=["get"], url_path="click")
    def click(self, request, pk=None):
        ad = self.get_object()

        # Record a click for the ad
        ip = request.META.get("REMOTE_ADDR")
        AdClick.objects.create(ad=ad, ip=ip)

        return Response({"redirect_to": ad.link}, status=status.HTTP_302_FOUND)