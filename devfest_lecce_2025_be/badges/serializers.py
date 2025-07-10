from rest_framework import serializers
from .models import Badge


class BadgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Badge
        fields = [
            "id",
            "name",
            "description",
            "picture",
        ]
