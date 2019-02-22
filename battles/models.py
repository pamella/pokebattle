import datetime

from django.db import models

from pokemons.models import Pokemon
from users.models import User


class Battle(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True)
    trainer_creator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="battle_creator"
    )
    trainer_opponent = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="battle_opponent"
    )
    status = models.CharField(max_length=56, default=1)
    trainer_winner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="battle_winner",
        null=True
    )

    def __str__(self):
        trainer_creator = str(self.trainer_creator).split("@")[0]
        trainer_opponent = str(self.trainer_opponent).split("@")[0]
        date = datetime.datetime.strftime(self.datetime_created, "%m-%d-%Y")
        return "Battle {}: {} vs {}, AT {}".format(
            self.id,
            trainer_creator,
            trainer_opponent,
            date
        )


class TrainerTeam(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon_1 = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        related_name="pokemon_1",
        null=True
    )
    pokemon_2 = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        related_name="pokemon_2",
        null=True
    )
    pokemon_3 = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        related_name="pokemon_3",
        null=True
    )
    battle_related = models.ForeignKey(
        Battle, on_delete=models.CASCADE,
        related_name="battle",
        null=True
    )

    def __str__(self):
        trainer = str(self.trainer).split("@")[0]
        return "Battle {} | TrainerTeam: {}".format(self.battle_related.id, trainer)
