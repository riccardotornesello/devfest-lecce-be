from rest_framework import serializers

from .models import Conference


class ConferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conference
        fields = [
            "id",
            "name",
            "note",
            "picture",
            "start_time",
            "end_time",
            "speaker",  # TODO: nested
            "topic",
            "typology",
            "level",
            "language",
        ]
