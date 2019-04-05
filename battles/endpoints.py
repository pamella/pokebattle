from django.db.models import Q

from rest_framework import generics, permissions

from battles.models import Battle
from battles.permissions import IsTrainerInBattle
from battles.serializers import BattleReadSerializer, ListBattleSerializer


class DetailBattleEndpoint(generics.RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleReadSerializer
    permission_classes = [IsTrainerInBattle]


class ListBattleEndpoint(generics.ListAPIView):
    queryset = Battle.objects.all()
    serializer_class = ListBattleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        queryset = Battle.objects.filter(
            Q(trainer_creator=user) | Q(trainer_opponent=user)
        )
        return queryset
