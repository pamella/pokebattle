from rest_framework import serializers

from battles.models import Battle, TrainerTeam
from pokemons.models import Pokemon
from pokemons.serializers import PokemonSerializer
from users.models import User


class BattleReadSerializer(serializers.ModelSerializer):
    user_queryset = User.objects.all()
    trainer_creator_id = serializers.PrimaryKeyRelatedField(
        source='trainer_creator.id', queryset=user_queryset)
    trainer_creator_email = serializers.CharField(source='trainer_creator.email')
    trainer_opponent_id = serializers.PrimaryKeyRelatedField(
        source='trainer_opponent.id', queryset=user_queryset)
    trainer_opponent_email = serializers.CharField(source='trainer_opponent.email')
    trainer_winner_id = serializers.PrimaryKeyRelatedField(
        source='trainer_winner.id', queryset=user_queryset, allow_null=True)
    trainer_winner_email = serializers.CharField(
        source='trainer_winner.email', allow_null=True)

    rounds = serializers.SerializerMethodField()

    class Meta:
        model = Battle
        fields = (
            'id',
            'status',
            'trainer_creator_id', 'trainer_creator_email',
            'trainer_opponent_id', 'trainer_opponent_email',
            'trainer_winner_id', 'trainer_winner_email',
            'rounds',
        )

    def get_rounds(self, obj):
        teams = obj.teams.all()
        rounds = [{}, {}, {}]
        for team in teams:
            is_creator = team.trainer == obj.trainer_creator
            role = 'creator_pokemon' if is_creator else 'opponent_pokemon'
            rounds[0][role] = PokemonSerializer(team.pokemon_1).data
            rounds[1][role] = PokemonSerializer(team.pokemon_2).data
            rounds[2][role] = PokemonSerializer(team.pokemon_3).data

        return rounds


class ListBattleSerializer(BattleReadSerializer):
    is_trainer_creator = serializers.SerializerMethodField()

    class Meta:
        model = Battle
        fields = (
            'id',
            'status',
            'trainer_creator_id', 'trainer_creator_email',
            'trainer_opponent_id', 'trainer_opponent_email',
            'trainer_winner_id', 'trainer_winner_email',
            'is_trainer_creator',
            'rounds',
        )

    def get_is_trainer_creator(self, obj):
        user = self.context['request'].user
        return user == obj.trainer_creator


class CreateBattleSerializer(serializers.ModelSerializer):
    trainer_creator = serializers.SerializerMethodField()
    pokemon_1 = serializers.CharField(max_length=56)
    pokemon_2 = serializers.CharField(max_length=56)
    pokemon_3 = serializers.CharField(max_length=56)
    order_1 = serializers.IntegerField()
    order_2 = serializers.IntegerField()
    order_3 = serializers.IntegerField()

    class Meta:
        model = Battle
        fields = (
            'trainer_creator', 'trainer_opponent',
            'pokemon_1', 'pokemon_2', 'pokemon_3',
            'order_1', 'order_2', 'order_3',
        )

    def get_trainer_creator(self, obj): # noqa
        user = self.context['request'].user
        return user.id

    def create(self, validated_data):
        validated_data['trainer_creator'] = User.objects.get(id=self.data['trainer_creator'])
        pokemons = [0, 1, 2]
        pokemons[validated_data.pop('order_1')] = validated_data.pop('pokemon_1')
        pokemons[validated_data.pop('order_2')] = validated_data.pop('pokemon_2')
        pokemons[validated_data.pop('order_3')] = validated_data.pop('pokemon_3')
        battle = super().create(validated_data)
        TrainerTeam.objects.create(
            trainer=validated_data['trainer_creator'],
            pokemon_1=Pokemon.objects.get(name=pokemons[0]),
            pokemon_2=Pokemon.objects.get(name=pokemons[1]),
            pokemon_3=Pokemon.objects.get(name=pokemons[2]),
            battle_related=battle,
        )
        return battle
