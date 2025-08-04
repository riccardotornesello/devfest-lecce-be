from rest_framework import serializers

from .models import Speaker


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ["id", "bio", "name", "country", "picture"]
