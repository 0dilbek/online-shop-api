from django.urls import path

from .views import AdvertisementDetailView, AdvertisementListView


urlpatterns = [
    path('ads/', AdvertisementListView.as_view(), name='ad-list'),
    path('ads/<int:pk>/', AdvertisementDetailView.as_view(), name='ad-detail'),
]
