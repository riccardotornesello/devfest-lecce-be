from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .models import Speaker
from .serializers import SpeakerSerializer


class SpeakerListView(ListAPIView):
    """
    API view to retrieve the list of speakers.
    """

    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
