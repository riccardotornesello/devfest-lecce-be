from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Badge, BadgeCode, OwnBadge
from .serializers import BadgeScanSerializer, BadgeSerializer


class BadgeListView(ListAPIView):
    """
    API view to retrieve the list of badges.
    If the user is authenticated, the queryset will include the badges they own.
    """

    serializer_class = BadgeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.request.user.uid if self.request.user else None

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

    serializer_class = BadgeScanSerializer
    queryset = Badge.objects.none()

    @swagger_auto_schema(
        request_body=BadgeScanSerializer,
        responses={
            201: BadgeSerializer,
            404: "Badge not found.",
            400: "Invalid request.",
        },
    )
    def post(self, request, *args, **kwargs):
        user_id = self.request.user.uid

        data_serializer = BadgeScanSerializer(data=request.data)
        if not data_serializer.is_valid():
            return Response(data_serializer.errors, status=400)

        secret = data_serializer.validated_data["secret"].lower()

        try:
            badge_code = BadgeCode.objects.get(code__iexact=secret)
        except BadgeCode.DoesNotExist:
            return Response({"detail": "Code not valid."}, status=404)

        # Check which badges are new
        new_badges = badge_code.badges.exclude(own_badges__user_id=user_id)
        OwnBadge.objects.bulk_create(
            [OwnBadge(badge=badge, user_id=user_id) for badge in new_badges]
        )

        return Response(BadgeSerializer(new_badges, many=True).data, status=201)
