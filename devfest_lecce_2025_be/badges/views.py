from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .models import Badge
from .serializers import BadgeSerializer


class BadgeListView(ListAPIView):
    """
    API view to retrieve the list of badges.
    """

    queryset = Badge.objects.all()  # TODO: sorting
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
