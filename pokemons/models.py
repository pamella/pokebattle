from django.db import models


class Pokemon(models.Model):
    api_id = models.SmallIntegerField(verbose_name='PokeAPI Id')
    name = models.CharField(max_length=20)
    sprite = models.URLField()

    attack = models.IntegerField()
    defense = models.IntegerField()
    hitpoints = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Pokemons"
