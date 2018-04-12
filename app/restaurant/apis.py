from collections import OrderedDict

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D

from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FoodCategorySerializer, RestaurantSerializer
from .models import FoodCategory, Restaurant


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000
    result_name = 'results'
    params_name = None

    def paginate_queryset(self, queryset, request, view=None):
        if hasattr(view, 'result_name'):
            self.result_name = view.result_name
        if hasattr(view, 'params_name'):
            self.params_name = view.params_name

        return super(StandardResultsSetPagination, self).paginate_queryset(queryset, request, view=None)

    def get_paginated_response(self, data):
        if self.params_name:
            if self.request.method == "GET":
                params = self.request.query_params

            if self.request.method == "POST":
                params = self.request.data

            res = Response(OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                (self.params_name, params),
                (self.result_name, data),
            ]))
        else:
            res = Response(OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                (self.result_name, data),
            ]))
        return res


class RestaurantView(ListAPIView):
    serializer_class = RestaurantSerializer
    pagination_class = StandardResultsSetPagination
    result_name = 'restaurants'
    params_name = 'search_params'

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            return self.list(request, *args, **kwargs)

    def get_queryset(self):
        lat = float(self.request.query_params['lat'])
        lng = float(self.request.query_params['lng'])
        radius = self.request.query_params.get('radius', 1500)
        search_text = self.request.query_params.get('search_text', None)

        pnt = Point(lng, lat, srid=4326)
        queryset = Restaurant.objects.all()
        queryset = queryset.filter(geo_point__distance_lte=(pnt, D(m=radius)))
        queryset = queryset.annotate(distance=Distance('geo_point', pnt))

        if search_text is not None:
            queryset = queryset.filter(title__contains=search_text)

        return queryset.order_by('distance')


class FoodCategoryView(ListAPIView):
    serializer_class = FoodCategorySerializer
    pagination_class = StandardResultsSetPagination
    result_name = 'categories'

    def get_queryset(self):
        order_option = self.request.query_params.get('order', '')
        category_query = {
            '': FoodCategory.objects.all(),
            'cnt': FoodCategory.objects.annotate(restaurant_count=Count('restaurant')).order_by('-restaurant_count')
        }
        return category_query.get(order_option, FoodCategory.objects.all())
