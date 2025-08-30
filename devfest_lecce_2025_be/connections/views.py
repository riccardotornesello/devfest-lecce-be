from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer

from .models import Connection
from .serializers import ConnectionScanSerializer


class ConnectionListView(ListAPIView):
    queryset = Connection.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.uid
        return Connection.objects.filter(user_from_id=user_id).order_by("-created_at")

    def get(self, request):
        connections = self.get_queryset()
        users = [c.user_to for c in connections]
        return Response(UserSerializer(users, many=True).data)

    @swagger_auto_schema(
        request_body=ConnectionScanSerializer,
        responses={
            201: UserSerializer,
            404: "User not found",
        },
    )
    def post(self, request):
        user_id = request.user.uid

        if not User.objects.filter(id=user_id).exists():
            User.objects.create(id=user_id)

        serializer = ConnectionScanSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        scanned_user_id = serializer.validated_data["user_id"]
        user = User.objects.filter(id=scanned_user_id).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        if not Connection.objects.filter(
            user_from_id=user_id, user_to_id=scanned_user_id
        ).exists():
            Connection.objects.create(user_from_id=user_id, user_to_id=scanned_user_id)

        return Response(UserSerializer(user).data, status=201)
