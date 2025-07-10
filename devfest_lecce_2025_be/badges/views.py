from rest_framework.generics import ListAPIView
from rest_framework import permissions, viewsets
from .serializers import BadgeSerializer
from .models import Badge


class BadgeListView(ListAPIView):
    """
    API view to retrieve the list of badges.
    """

    queryset = Badge.objects.all()  # TODO: sorting
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
