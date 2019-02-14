import requests


POKEAPI_ROOT = 'https://pokeapi.co/api/v2/pokemon'


def get_pokemon_stats(name):
    url = f'{POKEAPI_ROOT}/{name}'
    aux = requests.get(url).json()['stats']
    stats = {
        'defense': aux[3]['base_stat'],
        'attack': aux[4]['base_stat'],
        'hitpoints': aux[5]['base_stat']
    }

    return stats
