from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Advertisement
from .serializers import AdvertisementSerializer


class AdvertisementListView(ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer


class AdvertisementDetailView(RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
