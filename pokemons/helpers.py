import requests

from battles.models import TrainerTeam
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

    for poke_arg in pokemons_args:
        for key in keys:
            stats.append(poke_arg[key])

    pokemons_sum = sum(stats)
    return pokemons_sum <= limit


def pokemon_exists(name):
    url = f'{POKEAPI_ROOT}/{name}'
    if requests.get(url).status_code == 404:
        return False
    return True


def get_pokemons_from_trainerteam(battle, trainer):
    trainerteam = TrainerTeam.objects.get(
        battle_related=battle, trainer=trainer)
    return [
        trainerteam.pokemon_1,
        trainerteam.pokemon_2,
        trainerteam.pokemon_3,
    ]


# task
def save_pokeapi_pokemons():
    url = requests.get(f'{POKEAPI_ROOT}/?limit=802')
    poke_api = url.json()
    for pokemon in poke_api['results']:
        if Pokemon.objects.filter(name=pokemon['name']).exists():
            continue

        pokemon_args = get_pokemon_args(pokemon['name'])
        Pokemon.objects.create(
            api_id=pokemon_args['api_id'],
            name=pokemon_args['name'],
            sprite=pokemon_args['sprite'],
            attack=pokemon_args['attack'],
            defense=pokemon_args['defense'],
            hitpoints=pokemon_args['hitpoints'],
        )
