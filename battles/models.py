import datetime

from django.db import models

from common.models import IndexedTimeStampedModel
from pokemons.models import Pokemon
from users.models import User


class Battle(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True)
    trainer_creator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="battles_creator"
    )
    trainer_opponent = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="battles_opponent"
    )
    status = models.CharField(max_length=56, default='ON_GOING')
    trainer_winner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="+",
        null=True
    )

    def __str__(self):
        trainer_creator = str(self.trainer_creator).split("@")[0]
        trainer_opponent = str(self.trainer_opponent).split("@")[0]
        date = datetime.datetime.strftime(self.datetime_created, "%m-%d-%Y")
        return f"Battle {self.id}: {trainer_creator} vs {trainer_opponent}, AT {date}"


class TrainerTeam(models.Model):
    trainer = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="teams"
    )
    pokemon_1 = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        related_name="+",
        null=True
    )
    pokemon_2 = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        related_name="+",
        null=True
    )
    pokemon_3 = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        related_name="+",
        null=True
    )
    battle_related = models.ForeignKey(
        Battle, on_delete=models.CASCADE,
        related_name="teams",
        null=True
    )

    def __str__(self):
        trainer = str(self.trainer).split("@")[0]
        return f"Battle {self.battle_related.id} | TrainerTeam: {trainer}"


class Invite(IndexedTimeStampedModel):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    invited = models.EmailField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Invite from {self.inviter.get_short_name()} to {self.invited}'
