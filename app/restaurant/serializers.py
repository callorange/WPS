from rest_framework import serializers

from .models import FoodCategory, Restaurant, RestaurantContact


class FoodCategorySerializer(serializers.ModelSerializer):
    restaurant_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = FoodCategory
        fields = ['uuid', 'name', 'logo_url', 'restaurant_count']


class RestaurantSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(write_only=True, required=True)
    lng = serializers.FloatField(write_only=True, required=True)
    radius = serializers.IntegerField(write_only=True, required=False, min_value=1, max_value=5000)
    search_text = serializers.CharField(write_only=True, required=False)

    r_status = serializers.CharField(read_only=True)
    r_visible = serializers.CharField(read_only=True)

    tags = FoodCategorySerializer(read_only=True, many=True)

    distance = serializers.SerializerMethodField()

    contact = serializers.StringRelatedField()

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

            'address1',
            'apt_suite',
            'city',
            'country',
            'postal_code',
            'region',
            'formatted_address',

            'latitude',
            'longtitude',
            'tags',

            'distance',
            'contact',
        ]

    def get_distance(self, obj):
        return obj.distance.m
