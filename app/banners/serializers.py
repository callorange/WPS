from rest_framework import serializers

from restaurant.models import Restaurant
from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    img_banner = serializers.ImageField(default='')

    class Meta:
        model = Banner
        fields = [
            'id',
            'order',
            'title',
            'sub_title',
            'content',
            'img_banner',
            'img_banner_url',
            'restaurant',
        ]

    def validate(self, data):
        if not data['img_banner'] and data['restaurant']:
            restaurant = Restaurant.objects.get(uuid=data['restaurant'])
            if restaurant.logos.filter(width=750).exists():
                data['img_banner_url'] = restaurant.logos.get(width=750).url
                return data
            if restaurant.logos.filter(is_default=True).exists():
                data['img_banner_url'] = restaurant.logos.get(is_default=True).url
                return data
            data['img_banner_url'] = restaurant.last().url
            return data
        return data


class BannerDetailSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(read_only=True)

    class Meta:
        model = Banner
        fields = '__all__'
