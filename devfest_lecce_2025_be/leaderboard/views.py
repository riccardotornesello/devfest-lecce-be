from badges.models import OwnBadge
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User


class LeaderboardView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(cache_page(60))  # Cache for 1 minute
    def get(self, request, *args, **kwargs):
        # Get max and only_valid from query params
        max_entries = int(request.query_params.get("max", 10))
        max_entries = min(max(max_entries, 1), 100)  # Clamp between 1 and 100

        only_valid = request.query_params.get("only_valid", "false").lower() == "true"

        badges_query = (
            OwnBadge.objects.select_related("badge")
            .values("user_id")
            .annotate(Sum("badge__points"))
            .order_by("-badge__points__sum")
        )

        user_ids = [entry["user_id"] for entry in badges_query]
        users = User.objects.filter(id__in=user_ids)
        user_dict = {user.id: user for user in users}

        response_data = []

        for entry in badges_query:
            user = user_dict.get(entry["user_id"])

            if only_valid and not user:
                continue

            response_data.append(
                {
                    "id": entry["user_id"],
                    "name": user.name if user else None,
                    "surname": user.surname if user else None,
                    "points": entry["badge__points__sum"],
                }
            )

        return Response(response_data[:max_entries])
