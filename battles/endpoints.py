from rest_framework import generics

from battles.models import Battle
from battles.serializers import BattleSerializer


class DetailBattleEndpoint(generics.RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
