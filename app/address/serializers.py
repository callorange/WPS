from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    search_text = serializers.CharField(max_length=200, min_length=2)