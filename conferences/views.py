from rest_framework.generics import ListAPIView
from rest_framework import permissions, viewsets
from .serializers import ConferenceSerializer
from .models import Conference


class ConferenceListView(ListAPIView):
    """
    API view to retrieve the list of conferences.
    """

    queryset = Conference.objects.order_by("start_time")
    serializer_class = ConferenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
