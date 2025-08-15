from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Conference
from .serializers import ConferenceSerializer


class ConferenceListView(ListAPIView):
    """
    API view to retrieve the list of conferences.
    """

    queryset = Conference.objects.order_by("start_time")
    serializer_class = ConferenceSerializer
    permission_classes = [AllowAny]
