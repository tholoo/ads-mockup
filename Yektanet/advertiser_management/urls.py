from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"advertisers", views.AdvertiserViewSet, basename="advertisers")
router.register(r"", views.AdViewSet, basename="ads")

app_name = "advertiser_management"
urlpatterns = [
    path("", include(router.urls)),
]
