from datetime import datetime

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from restaurant.serializers import RestaurantSerializer, ItemsSerializer
from .models import Order, OrderItems
from restaurant.models import Restaurant, Items


class DeliverySerializer(serializers.Serializer):
    """주문 요청 - delivery 영역"""
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    address = serializers.CharField(allow_null=True, allow_blank=True)
    address_detail = serializers.CharField(allow_null=True, allow_blank=True)
    comment = serializers.CharField(allow_null=True, allow_blank=True)
    date_time = serializers.CharField(allow_null=True, allow_blank=True, max_length=12, min_length=12)


class PaymentSerializer(serializers.Serializer):
    """주문 요청 - payment 영역"""
    method = serializers.CharField()
    num = serializers.CharField(max_length=19, min_length=19)


class OrderItemSerializer(serializers.Serializer):
    """주문 요청 - order>items>item 영역"""
    item = serializers.UUIDField()
    cnt = serializers.IntegerField()
    comment = serializers.CharField(allow_null=True, allow_blank=True)

    def validate_item(self, data):
        if Items.objects.filter(uuid=data).exists():
            return Items.objects.get(uuid=data)
        raise ValidationError("존재 하지 않는 상품 입니다.")


class OrderInfoSerailizer(serializers.Serializer):
    """주문 요청 - order>items 영역"""
    restaurant = serializers.UUIDField()
    items = OrderItemSerializer(many=True)
    comment = serializers.CharField(allow_null=True, allow_blank=True)

    def validate_restaurant(self, data):
        if Restaurant.objects.filter(uuid=data).exists():
            return Restaurant.objects.get(uuid=data)
        raise ValidationError("존재 하지 않는 식당 입니다.")


class OrderSerializer(serializers.Serializer):
    """주문 요청 정보 전체"""
    delivery = DeliverySerializer()
    payment = PaymentSerializer()
    order = OrderInfoSerailizer()
    member = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        # 예약시간이 있으면 파싱
        if attrs["delivery"]["date_time"]:
            delivery_time = datetime.strptime(attrs['delivery']['date_time'], '%Y%m%d%H%M')
            attrs["delivery"]["date_time"] = timezone.make_aware(delivery_time)
        else:
            attrs["delivery"]["date_time"] = None

        # 가격 총 합계 및 각 아이템별 가격 구하기
        price_total = 0
        for item in attrs["order"]["items"]:
            obj = item['item']
            item['price'] = int(obj.price)
            item['sub_total'] = int(obj.price * item['cnt'])
            price_total = int(price_total + item['sub_total'])
        attrs['price_total'] = price_total

        return attrs

    def create(self, validated_data):
        # 주문 정보 생성 및 상세 정보 생성. 트랜잭션 처리
        with transaction.atomic():
            order_obj = Order.objects.create(
                delivery_lat=validated_data['delivery']['lat'],
                delivery_lng=validated_data['delivery']['lng'],
                delivery_address=validated_data['delivery']['address'],
                delivery_address_detail=validated_data['delivery']['address_detail'],
                delivery_comment=validated_data['delivery']['comment'],
                delivery_date_time=validated_data['delivery']['date_time'],
                payment_method=validated_data['payment']['method'],
                payment_num=validated_data['payment']['num'],
                order_restaurant=validated_data['order']['restaurant'],
                order_comment=validated_data['order']['comment'],
                order_member=validated_data['member'],
                price_total=validated_data['price_total'],
            )
            for item in validated_data["order"]["items"]:
                OrderItems.objects.create(
                    order=order_obj,
                    item=item['item'],
                    price=item['price'],
                    cnt=item['cnt'],
                    sub_total=item['sub_total'],
                    comment=item['comment'],
                )
        return validated_data


class OrderInfoItemSerializer(serializers.ModelSerializer):
    """주문 정보 > 주문상품리스트용"""
    item = ItemsSerializer(read_only=True)
    price = serializers.SerializerMethodField()
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItems
        fields = [
            'item',
            'price',
            'cnt',
            'sub_total',
            'comment',
        ]

    def get_price(self, obj):
        return int(obj.price / 100)

    def get_sub_total(self, obj):
        return int(obj.sub_total / 100)


class OrderInfoSerializer(serializers.ModelSerializer):
    """주문 정보"""
    order_restaurant = RestaurantSerializer(read_only=True)
    order_status = serializers.SerializerMethodField()
    price_total = serializers.SerializerMethodField()
    order_items = OrderInfoItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'delivery_lat',
            'delivery_lng',
            'delivery_address',
            'delivery_address_detail',
            'delivery_comment',
            'delivery_date_time',
            'payment_method',
            'payment_num',
            'order_restaurant',
            'order_comment',
            'order_member',
            'order_status',
            'order_create_at',
            'price_total',

            'order_items',
        ]

    def get_price_total(self, obj):
        return int(obj.price_total / 100)

    def get_order_status(self, obj):
        return obj.get_order_status_display()