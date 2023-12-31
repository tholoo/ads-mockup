from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from .models import Ad, AdClick, Advertiser, AdView
from .serializers import AdSerializer, AdvertiserSerializer


class AdvertiserView(APIView):
    def get(self, request):
        advertisers = Advertiser.objects.prefetch_related("ads").all()

        # add a view for each ad
        ip = request.META.get("REMOTE_ADDR")
        AdView.objects.bulk_create([AdView(ad=ad, ip=ip) for ad in Ad.objects.all()])

        serializer = AdvertiserSerializer(advertisers, many=True)

        return Response(serializer.data)


class AdRedirectView(APIView):
    def get(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)

        # record a click for the ad
        ip = request.META.get("REMOTE_ADDR")
        AdClick.objects.create(ad=ad, ip=ip)

        return Response({"redirect_to": ad.link}, status=status.HTTP_302_FOUND)


class AdCreateAPIView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdRetrieveAPIView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
