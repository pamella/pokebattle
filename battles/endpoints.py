from rest_framework import generics

from battles.models import Battle
from battles.permissions import IsTrainerInBattle
from battles.serializers import BattleReadSerializer


class DetailBattleEndpoint(generics.RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleReadSerializer
    permission_classes = [IsTrainerInBattle]
