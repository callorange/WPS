from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    search_text = serializers.CharField(max_length=200, min_length=2)
    language = serializers.CharField(required=False)


class GeoSearchRequestSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    search_text = serializers.CharField(max_length=200, min_length=2)
    language = serializers.CharField(required=False)


class StaticMapSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
