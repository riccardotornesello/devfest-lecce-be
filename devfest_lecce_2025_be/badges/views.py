from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Badge, OwnBadge
from .serializers import BadgeScanSerializer, BadgeSerializer


class BadgeListView(ListAPIView):
    """
    API view to retrieve the list of badges.
    If the user is authenticated, the queryset will include the badges they own.
    """

    serializer_class = BadgeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.request.user if self.request.user else None

        return Badge.objects.prefetch_related(
            Prefetch(
                "own_badges",
                queryset=OwnBadge.objects.filter(user_id=user_id),
            )
        )


class ScanBadgeView(GenericAPIView):
    """
    API view to retrieve a badge by its secret.
    """

    serializer_class = BadgeSerializer

    @swagger_auto_schema(
        request_body=BadgeScanSerializer,
        responses={
            201: BadgeSerializer,
            404: "Badge not found.",
            400: "Invalid request.",
        },
    )
    def post(self, request, *args, **kwargs):
        user_id = self.request.user

        data_serializer = BadgeScanSerializer(data=request.data)
        if not data_serializer.is_valid():
            return Response(data_serializer.errors, status=400)

        secret = data_serializer.validated_data["secret"].lower()

        try:
            badge = Badge.objects.get(name__iexact=secret)
        except Badge.DoesNotExist:
            return Response({"detail": "Badge not found."}, status=404)

        # Check if the user already owns this badge
        owned_badge = OwnBadge.objects.filter(badge=badge, user_id=user_id).first()
        if not owned_badge:
            owned_badge = OwnBadge.objects.create(badge=badge, user_id=user_id)

        serializer = self.get_serializer(badge)
        return Response(serializer.data, status=201)
