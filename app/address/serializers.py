from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    search_text = serializers.CharField(max_length=200, min_length=2)


class GeoSearchRequestSerializer(serializers.Serializer):
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    search_text = serializers.CharField(max_length=200, min_length=2)
