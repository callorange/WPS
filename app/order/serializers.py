from rest_framework import serializers


class DeliverySerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()


class DeliverySerializer(serializers.Serializer):
    position = DeliverySerializer()
    address = serializers.CharField(allow_null=True, allow_blank=True)
    address_detail = serializers.CharField(allow_null=True, allow_blank=True)
    comment = serializers.CharField(allow_null=True, allow_blank=True)
    date_time = serializers.CharField(allow_null=True, allow_blank=True, max_length=12, min_length=12)


class PaymentSerializer(serializers.Serializer):
    form = serializers.CharField()
    num = serializers.CharField(max_length=19, min_length=19)


class OrderItemSerializer(serializers.Serializer):
    item = serializers.UUIDField()
    comment = serializers.CharField(allow_null=True, allow_blank=True)


class OrderInfoSerailizer(serializers.Serializer):
    restaurant = serializers.UUIDField()
    items = OrderItemSerializer(many=True)
    comment = serializers.CharField(allow_null=True, allow_blank=True)


class OrderSerializer(serializers.Serializer):
    delivery = DeliverySerializer()
    payment = PaymentSerializer()
    order = OrderInfoSerailizer()

    def create(self, validated_data):
        print(2, validated_data)
        return validated_data
