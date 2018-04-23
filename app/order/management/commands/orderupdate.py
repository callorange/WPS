from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.models import F
from django.utils import timezone

from ...models import Order


class Command(BaseCommand):
    help = '주문 정보 자동 업데이트 처리. 준비중->조리중. 조리중->배달중. 배달중->배달완료'

    def handle(self, *args, **options):
        #준비중에서 1분 이상 지난 주문을 조리중으로 업데이트
        query = Order.objects.filter(order_status='A', order_create_at__lte=timezone.now()-timedelta(minutes=1))
        query.update(order_status='B', order_making_at=timezone.now())

        #조리중에서 1분 이상 지난 주문을 배달중으로 업데이트
        query = Order.objects.filter(order_status='B', order_making_at__lte=timezone.now()-timedelta(minutes=1))
        query.update(order_status='C', order_delivery_at=timezone.now())

        #배달중에서 1분 이상 지난 주문을 배달완료 업데이트
        query = Order.objects.filter(order_status='C', order_delivery_at__lte=timezone.now()-timedelta(minutes=1))
        query.update(order_status='D', order_delivery_complete_at=timezone.now())
