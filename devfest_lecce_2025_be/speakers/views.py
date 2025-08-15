from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Speaker
from .serializers import SpeakerSerializer


class SpeakerListView(ListAPIView):
    """
    API view to retrieve the list of speakers.
    """

    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [AllowAny]
