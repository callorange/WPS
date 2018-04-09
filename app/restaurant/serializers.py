from rest_framework import serializers

from .models import FoodCategory


class FoodCategorySerializer(serializers.ModelSerializer):
    restaurant_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = FoodCategory
        fields = ['uuid', 'name', 'logo_url', 'restaurant_count']
