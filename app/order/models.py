from django.conf import settings
from django.db import models

from restaurant.models import Restaurant, Items


class Order(models.Model):
    ORDER_STATUS = (
        ('A', '준비중'),
        ('B', '조리중'),
        ('C', '배달중'),
        ('D', '배달완료'),
        ('F', '주문완료'),
        ('Z', '주문취소'),
    )

    delivery_lat = models.FloatField(default=0, verbose_name="배달위치 위도")
    delivery_lng = models.FloatField(default=0, verbose_name="배달위치 경도")
    delivery_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="배달 주소")
    delivery_address_detail = models.CharField(max_length=255, blank=True, null=True, verbose_name="배달 상세주소")
    delivery_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="배달요청사항")
    delivery_date_time = models.DateTimeField(default=None, blank=True, null=True, verbose_name="예약시간")

    payment_method = models.CharField(max_length=10, verbose_name="결제수단")
    payment_num = models.CharField(max_length=19, verbose_name="카드번호")

    order_restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders', verbose_name="식당")
    order_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="주문요청사항")
    order_member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="주문유저"
    )
    order_status = models.CharField(choices=ORDER_STATUS, default='A', max_length=1, verbose_name="주문상태")
    order_create_at = models.DateTimeField(auto_now_add=True)

    price_total = models.PositiveIntegerField(default=0, verbose_name="총 가격 합계")

    def __str__(self):
        return f'{self.order_member} - {self.pk}: {self.get_order_status_display()}'

    class Meta:
        verbose_name = '주문정보'
        verbose_name_plural = '주문정보들'
        ordering = ['-order_create_at']


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="주문")
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='order_items', verbose_name="상품")
    price = models.PositiveIntegerField(default=0, verbose_name="가격")
    cnt = models.PositiveIntegerField(default=0, verbose_name="수량")
    sub_total = models.PositiveIntegerField(default=0, verbose_name="가격 합계")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="요청사항")

    def __str__(self):
        return f'{self.order} - {self.item}'

    class Meta:
        verbose_name = '주문 상세'
        verbose_name_plural = '주문 상세 아이템들'
        ordering = ['order', 'pk']
