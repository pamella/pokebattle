# rounds figth
def get_pokemon_with_highest_hitpoints(pokemon_1, pokemon_2):
    return pokemon_1 if pokemon_1.hitpoints > pokemon_2.hitpoints else pokemon_2


def compare_attack_defense(pokemon_1, pokemon_2):
    if pokemon_1.attack > pokemon_2.defense:
        return pokemon_1
    return pokemon_2


def get_pokemon_round_winner(pokemon_1, pokemon_2):
    if compare_attack_defense(pokemon_1, pokemon_2) == compare_attack_defense(pokemon_2, pokemon_1):
        return compare_attack_defense(pokemon_1, pokemon_2)
    return get_pokemon_with_highest_hitpoints(pokemon_1, pokemon_2)


# battle fight
def get_battle_winner(battle):
    trainer_team_creator = battle.trainer_creator.teams.filter(battle_related=battle).first()
    trainer_team_opponent = battle.trainer_opponent.teams.filter(battle_related=battle).first()
    pokemons_creator = [
        trainer_team_creator.pokemon_1,
        trainer_team_creator.pokemon_2,
        trainer_team_creator.pokemon_3
    ]
    pokemons_opponent = [
        trainer_team_opponent.pokemon_1,
        trainer_team_opponent.pokemon_2,
        trainer_team_opponent.pokemon_3,
    ]
    rounds_trainers_winners = []

    for (pokemon_c, pokemon_o) in zip(pokemons_creator, pokemons_opponent):
        if get_pokemon_round_winner(pokemon_c, pokemon_o) == pokemon_c:
            rounds_trainers_winners.append('creator')
        else:
            rounds_trainers_winners.append('opponent')

    if rounds_trainers_winners.count('creator') > rounds_trainers_winners.count('opponent'):
        return battle.trainer_creator
    return battle.trainer_opponent


def run_battle(battle):
    battle.status = 'SETTLED'
    battle.trainer_winner = get_battle_winner(battle)
    return battle.save()


def order_battle_pokemons(cleaned_data):
    pokemons = [0, 1, 2]
    pokemons[int(cleaned_data['order_1'])] = cleaned_data['pokemon_1'].name
    pokemons[int(cleaned_data['order_2'])] = cleaned_data['pokemon_2'].name
    pokemons[int(cleaned_data['order_3'])] = cleaned_data['pokemon_3'].name
    return pokemons
