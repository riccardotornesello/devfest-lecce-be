from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .models import Conference
from .serializers import ConferenceSerializer


class ConferenceListView(ListAPIView):
    """
    API view to retrieve the list of conferences.
    """

    queryset = Conference.objects.order_by("start_time")
    serializer_class = ConferenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
