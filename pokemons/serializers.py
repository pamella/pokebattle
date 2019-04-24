from rest_framework import serializers

from pokemons.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='name')

    class Meta:
        model = Pokemon
        fields = (
            'id', 'api_id', 'name', 'sprite',
            'attack', 'defense', 'hitpoints',
            'value', 'label',
        )
