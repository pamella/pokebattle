# one-a-one figth
def compare_hitpoints(pokemon_1, pokemon_2):
    if pokemon_1.hitpoints > pokemon_2.hitpoints:
        return pokemon_1
    return pokemon_2


def compare_attack_defense(pokemon_1, pokemon_2):
    if pokemon_1.attack > pokemon_2.defense:
        return pokemon_1
    return pokemon_2


def get_one_a_one_fight_winner(pokemon_1, pokemon_2):
    if compare_attack_defense(pokemon_1, pokemon_2) == compare_attack_defense(pokemon_2, pokemon_1):
        return compare_attack_defense(pokemon_1, pokemon_2)
    return compare_hitpoints(pokemon_1, pokemon_2)


# battle fight
def get_battle_winner(one_a_one_results):
    print('one_a_one_results: ', one_a_one_results)
    if one_a_one_results.count('creator') > one_a_one_results.count('opponent'):
        return 'creator'
    return 'opponent'


def battle(pokemons_creator, pokemons_opponent):
    one_a_one_results = []
    for (pokemon_c, pokemon_o) in zip(pokemons_creator, pokemons_opponent):
        if get_one_a_one_fight_winner(pokemon_c, pokemon_o) == pokemon_c:
            one_a_one_results.append('creator')
        else:
            one_a_one_results.append('opponent')

    return get_battle_winner(one_a_one_results)
