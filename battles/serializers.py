from rest_framework import serializers

from battles.models import Battle, TrainerTeam


class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = '__all__'


class TrainerTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerTeam
        fields = '__all__'
