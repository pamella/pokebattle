from django.conf import settings
from django.urls import reverse_lazy

from templated_email import send_templated_mail


# send email
def send_battle_result_email(battle):
    battle.refresh_from_db()
    trainer_team_creator = battle.trainer_creator.teams.filter(battle_related=battle).first()
    trainer_team_opponent = battle.trainer_opponent.teams.filter(battle_related=battle).first()
    send_templated_mail(
        template_name='battle_result',
        from_email=settings.SERVER_EMAIL,
        recipient_list=[battle.trainer_creator.email],
        bcc=[battle.trainer_opponent.email],
        context={
            'trainer_creator': battle.trainer_creator.get_short_name(),
            'trainer_opponent': battle.trainer_opponent.get_short_name(),
            'trainer_winner': battle.trainer_winner.get_short_name(),
            'trainer_team_creator': trainer_team_creator,
            'trainer_team_opponent': trainer_team_opponent,
        }
    )


def send_battle_match_invite_email(battle):
    select_team_url = reverse_lazy('battles:select_team')
    challenge_back_url = f'{settings.HOST}{select_team_url}?id={battle.pk}'
    send_templated_mail(
        template_name='battle_match_invite',
        from_email=settings.SERVER_EMAIL,
        recipient_list=[battle.trainer_opponent.email],
        context={
            'trainer_creator': battle.trainer_creator.get_short_name(),
            'trainer_opponent': battle.trainer_opponent.get_short_name(),
            'challenge_back_url': challenge_back_url,
        }
    )


def send_invited_friend_email(invite):
    middle_url = reverse_lazy('users:signup')
    signup_url = f'{settings.HOST}{middle_url}'
    send_templated_mail(
        template_name='invite_friend',
        from_email=settings.SERVER_EMAIL,
        recipient_list=[invite.invited],
        context={
            'inviter': invite.inviter.get_short_name(),
            'invited': invite.invited,
            'signup_url': signup_url,
        }
    )
