from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import OrderSerializer


class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
