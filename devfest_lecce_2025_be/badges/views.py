from app.authentication import FirebaseAuthentication
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


class ScanBadgeView(APIView):
    """
    API view to retrieve a badge by its secret.
    """

    serializer_class = BadgeSerializer
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = self.request.user

        secret = request.data.get("secret")
        if not secret:
            return Response({"detail": "Secret is required."}, status=400)

        try:
            badge = Badge.objects.get(secret=secret)
        except Badge.DoesNotExist:
            return Response({"detail": "Badge not found."}, status=404)

        # Check if the user already owns this badge
        owned_badge = OwnBadge.objects.filter(badge=badge, user_id=user_id).first()
        if not owned_badge:
            owned_badge = OwnBadge.objects.create(badge=badge, user_id=user_id)

        return Response(
            BadgeSerializer(badge).data,
            status=200,
        )
