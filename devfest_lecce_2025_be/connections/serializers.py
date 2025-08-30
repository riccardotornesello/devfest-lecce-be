from rest_framework import serializers


class ConnectionScanSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
