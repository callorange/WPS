from django.urls import resolve
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order
from restaurant.apis import StandardResultsSetPagination
from .serializers import OrderSerializer, OrderInfoSerializer


class OrderCreateView(CreateAPIView):
    """주문 정보 생성"""
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)


class OrderListView(ListAPIView):
    """주문 내역"""
    serializer_class = OrderInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = StandardResultsSetPagination
    page_result_name = 'orders'

    def get_queryset(self):
        # 접근한 URL Name에 따라서 다른 쿼리셋을 반환한다.
        r = resolve(self.request.path)
        query = {
            'list-prepare': Order.objects.filter(order_member=self.request.user).filter(
                order_status__in=['A', 'B', 'C']),
            'list-past': Order.objects.filter(order_member=self.request.user).filter(order_status__in=['D', 'F', 'Z']),
            'list': Order.objects.filter(order_member=self.request.user),
        }
        return query.get(r.url_name, query['list'])


class OrderView(APIView):
    """주문 정보(단건) 보기 및 정보 업데이트"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # URL에서 pk값을 받아온다.
        pk = kwargs.get('pk', '')

        # pk값과 인증여부 확인
        if pk and request.user.is_authenticated:
            # DB에 해당 주문번호 및 유저가 맞는지 확인 후 리턴
            if Order.objects.filter(pk=pk, order_member=request.user).exists():
                order_obj = Order.objects.get(pk=pk, order_member=request.user)
                serialize = OrderInfoSerializer(order_obj, context={'request': request})
                return Response(serialize.data, status=status.HTTP_200_OK, content_type='application/json')
            raise ValidationError('요청하신 정보를 찾을 수 없습니다.', 404)
        raise ValidationError('잘못된 요청입니다.', 400)

    def put(self, request, *args, **kwargs):
        # URL에서 pk값을 받아온다.
        pk = kwargs.get('pk', '')

        # pk값과 인증여부 확인
        if pk and request.user.is_authenticated:
            if Order.objects.filter(pk=pk, order_member=request.user).exists():
                order_obj = Order.objects.get(pk=pk, order_member=request.user)

                # 준비중이면 취소로 업데이트
                if order_obj.order_status == 'A':
                    order_obj.order_status = 'Z'
                    order_obj.save()
                # 배달완료면 주문완료로 업데이트
                elif order_obj.order_status == 'D':
                    order_obj.order_status = 'F'
                    order_obj.save()
                # 다른 상태에선 업데이트 불가
                else:
                    raise ValidationError('취소/완료가 불가능 합니다.', 403)

                # 정상 완료
                serialize = OrderInfoSerializer(order_obj, context={'request': request})
                return Response(serialize.data, status=status.HTTP_200_OK, content_type='application/json')

            raise ValidationError('요청하신 정보를 찾을 수 없습니다.', 404)
        raise ValidationError('잘못된 요청입니다.', 400)
