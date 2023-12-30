from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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


class AdAPIView(APIView):
    def get(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ad = serializer.save()
        return Response(AdSerializer(ad).data, status=status.HTTP_201_CREATED)
