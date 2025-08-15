from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Room
from .serializers import RoomSerializer


class RoomListView(ListAPIView):
    """
    API view to retrieve the list of rooms.
    """

    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [AllowAny]
