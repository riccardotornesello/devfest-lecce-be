from rest_framework import serializers
from .models import Conference


class ConferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conference
        fields = [
            "id",
            "name",
            "note",
            "start_time",
            "end_time",
            "speaker",
            "topic",
            "typology",
            "level",
            "language",
        ]
