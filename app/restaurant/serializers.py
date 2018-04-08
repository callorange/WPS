from rest_framework import serializers

from .models import FoodCategory


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = '__all__'
