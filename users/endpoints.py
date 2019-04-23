from rest_framework import generics, permissions

from users.models import User
from users.serializers import UserSerializer


class ListUserEndpoint(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(email=self.request.user.email)
