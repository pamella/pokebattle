from rest_framework import serializers

from pokemons.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = (
            'id', 'api_id', 'name', 'sprite',
            'attack', 'defense', 'hitpoints',
        )
