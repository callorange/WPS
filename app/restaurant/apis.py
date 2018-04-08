from collections import OrderedDict

from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FoodCategorySerializer
from .models import FoodCategory


class Restaurant(APIView):
    pass


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('categories', data)
        ]))


class FoodCategoryView(ListAPIView):
    model = FoodCategory
    serializer_class = FoodCategorySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        order_option = self.request.query_params.get('order', '')
        category_query = {
            '': FoodCategory.objects.all(),
            'cnt': FoodCategory.objects.annotate(restaurant_count=Count('restaurant')).order_by('-restaurant_count')
        }
        return category_query.get(order_option, FoodCategory.objects.all())
