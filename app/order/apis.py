from django.urls import resolve
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order
from restaurant.apis import StandardResultsSetPagination
from .serializers import OrderSerializer, OrderListSerializer


class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)


class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = StandardResultsSetPagination
    page_result_name = 'orders'

    def get_queryset(self):
        r = resolve(self.request.path)
        query = {
            'list-prepare': Order.objects.filter(order_member=self.request.user).filter(order_status__in=['A', 'B', 'C']),
            'list-past': Order.objects.filter(order_member=self.request.user).filter(order_status__in=['D', 'Z']),
            'list': Order.objects.filter(order_member=self.request.user),
        }
        return query.get(r.url_name, query['list'])
