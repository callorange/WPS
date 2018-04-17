from rest_framework import generics

from .serializers import BannerSerializer
from .models import Banner


class BannerListCreateView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
