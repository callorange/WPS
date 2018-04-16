import math

from rest_framework import serializers

from .models import FoodCategory, Restaurant, RestaurantContact, RestaurantLogo, RestaurantSectionHours, MenuSections, \
    Items


class FoodCategorySerializer(serializers.ModelSerializer):
    restaurant_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = FoodCategory
        fields = ['uuid', 'name', 'logo_url', 'restaurant_count']


class RestaurantLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantLogo
        fields = '__all__'


class RestaurantSectionHoursSerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantSectionHours
        fields = [
            'day_of_week',
            'day_of_week_display',
            'start_time',
            'end_time',
        ]

    def get_day_of_week_display(self, obj):
        return obj.get_day_of_week_display()


class RestaurantSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(write_only=True, required=True)
    lng = serializers.FloatField(write_only=True, required=True)
    radius = serializers.IntegerField(write_only=True, required=False, min_value=1)
    search_text = serializers.CharField(write_only=True, required=False)

    r_status = serializers.CharField(read_only=True)
    r_visible = serializers.CharField(read_only=True)
    address = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    eta_range = serializers.SerializerMethodField()

    tags = FoodCategorySerializer(read_only=True, many=True)
    logo = serializers.SerializerMethodField()
    logos = RestaurantLogoSerializer(read_only=True, many=True)
    open_time = RestaurantSectionHoursSerializer(read_only=True, many=True)
    contact = serializers.StringRelatedField(many=True)

    class Meta:
        model = Restaurant
        fields = [
            'lat',
            'lng',
            'radius',
            'search_text',

            'uuid',
            'title',
            'r_status',
            'r_visible',
            'schedule_order',
            'rating',

            'address',
            'position',
            'eta_range',

            'tags',
            'logo',
            'logos',
            'open_time',
            'contact',
        ]

    def get_position(self, obj):
        return {
            'latitude': obj.latitude,
            'longtitude': obj.longtitude,
            'distance': int(obj.distance.m),
        }

    def get_eta_range(self, obj):
        return {
            'min': 20+math.ceil(obj.distance.m/1000)*5,
            'max': 30+math.ceil(obj.distance.m/1000)*5,
        }

    def get_address(self, obj):

        return {
            'address1': obj.address1,
            'apt_suite': obj.apt_suite,
            'city': obj.city,
            'country': obj.country,
            'postal_code': obj.postal_code,
            'region': obj.region,
            'formatted_address': obj.formatted_address,
        }

    def get_logo(self, obj):
        agent = self.context['request'].META.get('HTTP_USER_AGENT', '').lower()
        if 'iphone' in agent or 'ipad' in agent:
            if obj.logos.filter(width=750).exists():
                return obj.logos.get(width=750).url

        if obj.logos.filter(is_default=True).exists():
            return obj.logos.get(is_default=True).url

        return obj.logos.last().url


class ItemsSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Items
        fields = '__all__'

    def get_price(self, obj):
        return int(obj.price / 100)


class RestaurantMenuSerializer(serializers.ModelSerializer):
    items = ItemsSerializer(many=True, read_only=True)

    class Meta:
        model = MenuSections
        fields = [
            'uuid',
            'title',

            'items',
        ]
