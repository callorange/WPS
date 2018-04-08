from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FoodCategorySerializer
from .models import FoodCategory


class Restaurant(APIView):
    pass


class FoodCategoryView(APIView):

    def get(self, request, format=None):
        serializer = FoodCategorySerializer(FoodCategory.objects.all(), many=True)
        return Response({'categories': serializer.data}, status=status.HTTP_200_OK)
