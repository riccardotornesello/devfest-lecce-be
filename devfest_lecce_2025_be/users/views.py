from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.uid
        return User.objects.filter(id=user_id)

    def get(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        if not user:
            user = User.objects.create(id=self.request.user.uid)

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        if not user:
            user = User.objects.create(id=self.request.user.uid)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        if user:
            user.delete()
        return Response(status=204)
