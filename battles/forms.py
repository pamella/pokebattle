from django import forms

from battles.helpers import get_pokemon_stats
from battles.models import Battle, TrainerTeam
from pokemons.models import Pokemon


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ('trainer_opponent', 'trainer_creator')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trainer_creator'].initial = self.initial['user'].id
        self.fields['trainer_creator'].widget = forms.HiddenInput()

        pkm1 = forms.CharField()
        pkm2 = forms.CharField()
        pkm3 = forms.CharField()
        self.fields['pkm1'] = pkm1
        self.fields['pkm2'] = pkm2
        self.fields['pkm3'] = pkm3

    def save(self, commit=True):
        pokemons = {
            'pkm1': self.cleaned_data['pkm1'].strip(),
            'pkm2': self.cleaned_data['pkm2'].strip(),
            'pkm3': self.cleaned_data['pkm3'].strip()
        }
        self.instance.save()

        for key in pokemons:
            if Pokemon.objects.filter(name=pokemons[key]).count() == 0:
                Pokemon.objects.create(
                    name=pokemons[key],
                    attack=get_pokemon_stats(pokemons[key])['attack'],
                    defense=get_pokemon_stats(pokemons[key])['defense'],
                    hitpoints=get_pokemon_stats(pokemons[key])['hitpoints'],
                )

        TrainerTeam.objects.create(
            trainer=self.initial['user'],
            pokemon_1=Pokemon.objects.get(name=pokemons['pkm1']),
            pokemon_2=Pokemon.objects.get(name=pokemons['pkm2']),
            pokemon_3=Pokemon.objects.get(name=pokemons['pkm2']),
            battle_related=self.instance,
        )

        return super().save()
