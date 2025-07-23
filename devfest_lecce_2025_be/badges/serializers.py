from rest_framework import serializers

from .models import Badge


class BadgeSerializer(serializers.ModelSerializer):
    owned = serializers.SerializerMethodField()

    def get_owned(self, obj):
        return obj.own_badges.count() > 0 if obj.own_badges else False

    class Meta:
        model = Badge
        fields = ["id", "name", "description", "picture", "owned"]
