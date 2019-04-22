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

    class Meta:
        model = Battle
        fields = (
            'trainer_creator', 'trainer_opponent',
        )

    def get_trainer_creator(self, obj): # noqa
        user = self.context['request'].user
        return user.id

    def create(self, validated_data):
        validated_data['trainer_creator'] = User.objects.get(id=self.data['trainer_creator'])
        pokemon_1 = self.context['request'].data['pokemon_1']
        pokemon_2= self.context['request'].data['pokemon_1']
        pokemon_3 = self.context['request'].data['pokemon_1']
        import ipdb; ipdb.set_trace()
        # validated_data['pokemon_1'] = Pokemon.objects.get(name=self.data['pokemon_1'])
        return super().create(validated_data)
