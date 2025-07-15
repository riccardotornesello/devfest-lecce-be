from rest_framework import serializers
from speakers.serializers import SpeakerSerializer

from .models import Conference, ConferenceTopic, ConferenceType


class ConferenceTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceTopic
        fields = ["id", "name"]


class ConferenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceType
        fields = ["id", "name"]


class ConferenceSerializer(serializers.ModelSerializer):
    topic = ConferenceTopicSerializer()
    typology = ConferenceTypeSerializer()
    speaker = SpeakerSerializer()

    class Meta:
        model = Conference
        fields = [
            "id",
            "name",
            "note",
            "picture",
            "start_time",
            "end_time",
            "speaker",
            "topic",
            "typology",
            "level",
            "language",
        ]
