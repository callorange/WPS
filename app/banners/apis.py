from rest_framework import generics

from .serializers import BannerSerializer, BannerDetailSerializer
from .models import Banner


class BannerListCreateView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class BannerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerDetailSerializer
    lookup_field = 'order'
    lookup_url_kwarg = 'order'
