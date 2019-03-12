from django.conf import settings
from django.urls import reverse_lazy

from templated_email import send_templated_mail

from battles.models import TrainerTeam


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
def get_battle_winner(pokemons_creator, pokemons_opponent):
    one_a_one_results = []
    for (pokemon_c, pokemon_o) in zip(pokemons_creator, pokemons_opponent):
        if get_one_a_one_fight_winner(pokemon_c, pokemon_o) == pokemon_c:
            one_a_one_results.append('creator')
        else:
            one_a_one_results.append('opponent')

    if one_a_one_results.count('creator') > one_a_one_results.count('opponent'):
        return 'creator'
    return 'opponent'


# send email
def generate_challenge_back_url(battle):
    select_team_url = reverse_lazy('battles:select_team')
    challenge_back_url = f'{settings.HOST}{select_team_url}?id={battle.pk}'
    return challenge_back_url


def send_battle_result_email(battle):
    trainers = [battle.trainer_creator, battle.trainer_opponent]
    for trainer in trainers:
        trainer_opponent = trainers[1] if trainer == trainers[0] else trainers[0]
        trainer_team = TrainerTeam.objects.get(battle_related=battle, trainer=trainer)
        trainer_opponent_team = TrainerTeam.objects.get(
            battle_related=battle,
            trainer=trainer_opponent
        )
        send_templated_mail(
            template_name='battle_result',
            from_email=settings.SERVER_EMAIL,
            recipient_list=[trainer.email],
            context={
                'trainer': trainer.get_short_name(),
                'trainer_opponent': trainer_opponent.get_short_name(),
                'winner': battle.trainer_winner.get_short_name(),
                'trainer_team': trainer_team,
                'trainer_opponent_team': trainer_opponent_team,
            }
        )


def send_battle_match_invite(battle):
    send_templated_mail(
        template_name='battle_match_invite',
        from_email=settings.SERVER_EMAIL,
        recipient_list=[battle.trainer_opponent.email],
        context={
            'trainer_creator': battle.trainer_creator.get_short_name(),
            'trainer_opponent': battle.trainer_opponent.get_short_name(),
            'challenge_back_url': generate_challenge_back_url(battle)
        }
    )
