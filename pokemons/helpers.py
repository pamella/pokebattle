import requests

from pokemons.models import Pokemon


POKEAPI_ROOT = 'https://pokeapi.co/api/v2/pokemon'


def get_pokemon_args(name):
    url = f'{POKEAPI_ROOT}/{name}'
    poke_api = requests.get(url).json()
    pokemon_args = {
        'api_id': poke_api['id'],
        'name': poke_api['name'],
        'sprite': poke_api['sprites']['front_default'],
        'defense': poke_api['stats'][3]['base_stat'],
        'attack': poke_api['stats'][4]['base_stat'],
        'hitpoints': poke_api['stats'][5]['base_stat']
    }

    return pokemon_args


def is_pokemons_sum_valid(pokemons):
    limit = 600
    keys = ['defense', 'attack', 'hitpoints']
    pokemons_args = [get_pokemon_args(pokemon) for pokemon in pokemons]
    stats = []

    for i in range(0, 3):
        for x in keys:
            stats.append(pokemons_args[i][x])

    pokemons_sum = sum(stats)
    return pokemons_sum <= limit


def pokemon_exists(name):
    url = f'{POKEAPI_ROOT}/{name}'
    if requests.get(url).status_code == 404:
        return False
    return True


def get_pokemons_from_trainerteam(trainerteam):
    return {
        '0': Pokemon.objects.get(name=trainerteam.pokemon_1),
        '1': Pokemon.objects.get(name=trainerteam.pokemon_2),
        '2': Pokemon.objects.get(name=trainerteam.pokemon_3),
    }
