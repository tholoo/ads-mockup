from django.urls import path

from . import views


app_name = "advertiser_management"
urlpatterns = [
    path("", views.AdCreateAPIView.as_view(), name="ads_list"),
    path("<int:pk>/", views.AdRetrieveAPIView.as_view(), name="ads_detail"),
    path("all/", views.AdvertiserView.as_view(), name="ads"),
    path("click/<int:pk>/", views.AdRedirectView.as_view(), name="ads_click"),
]
