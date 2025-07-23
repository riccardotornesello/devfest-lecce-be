from app.authentication import FirebaseAuthentication
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView

from .models import Badge, OwnBadge
from .serializers import BadgeSerializer


class BadgeListView(ListAPIView):
    """
    API view to retrieve the list of badges.
    If the user is authenticated, the queryset will include the badges they own.
    """

    serializer_class = BadgeSerializer
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self):
        user_id = self.request.user if self.request.user else None

        return Badge.objects.prefetch_related(
            Prefetch(
                "own_badges",
                queryset=OwnBadge.objects.filter(user_id=user_id),
            )
        )
