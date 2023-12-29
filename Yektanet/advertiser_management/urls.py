from django.urls import path

from . import views


app_name = "advertiser_management"
urlpatterns = [
    path("all/", views.AdvertiserView.as_view(), name="ads"),
    path("click/<int:pk>/", views.AdRedirectView.as_view(), name="ads_click"),
    path("<int:pk>/", views.AdAPIView.as_view(), name="ads_detail"),
]
