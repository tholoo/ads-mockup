from django.urls import path

from . import views


app_name = "advertiser_management"
urlpatterns = [
    path("", views.AdvertiserView.as_view(), name="ads"),
    path("click/<int:pk>/", views.AdRedirectView.as_view(), name="ads_click"),
    path("create/", views.AdCreateView.as_view(), name="ads_create"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="ads_detail"),
]
