from django import forms

from battles.models import Battle, TrainerTeam
from pokemons.helpers import get_pokemon_stats, is_pokemons_sum_valid
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
        self.fields['pokemon_1'] = pkm1
        self.fields['pokemon_2'] = pkm2
        self.fields['pokemon_3'] = pkm3

    def clean(self):
        cleaned_data = super().clean()
        pokemons = [
            self.cleaned_data['pokemon_1'].lower().strip(),
            self.cleaned_data['pokemon_2'].lower().strip(),
            self.cleaned_data['pokemon_3'].lower().strip()
        ]

        if not is_pokemons_sum_valid(pokemons):
            raise forms.ValidationError(
                'Trainer, your pokemon team stats can not sum more than 600 points.'
            )

        return cleaned_data

    def save(self, commit=True):
        pokemons = [
            self.cleaned_data['pokemon_1'].lower().strip(),
            self.cleaned_data['pokemon_2'].lower().strip(),
            self.cleaned_data['pokemon_3'].lower().strip()
        ]
        self.instance.save()

        for pokemon in pokemons:
            if Pokemon.objects.filter(name=pokemon).count() == 0:
                Pokemon.objects.create(
                    name=pokemon,
                    attack=get_pokemon_stats(pokemon)['attack'],
                    defense=get_pokemon_stats(pokemon)['defense'],
                    hitpoints=get_pokemon_stats(pokemon)['hitpoints'],
                )

        TrainerTeam.objects.create(
            trainer=self.initial['user'],
            pokemon_1=Pokemon.objects.get(name=pokemons[0]),
            pokemon_2=Pokemon.objects.get(name=pokemons[1]),
            pokemon_3=Pokemon.objects.get(name=pokemons[2]),
            battle_related=self.instance,
        )

        return super().save()


class SelectTrainerTeamForm(forms.ModelForm):
    class Meta:
        model = TrainerTeam
        fields = ('trainer', 'battle_related')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trainer'].initial = self.initial['user'].id
        self.fields['trainer'].widget = forms.HiddenInput()
        self.fields['battle_related'].initial = self.initial['battle']
        self.fields['battle_related'].widget = forms.HiddenInput()

        pkm1 = forms.CharField()
        pkm2 = forms.CharField()
        pkm3 = forms.CharField()
        self.fields['pokemon_1'] = pkm1
        self.fields['pokemon_2'] = pkm2
        self.fields['pokemon_3'] = pkm3

    def clean(self):
        cleaned_data = super().clean()
        pokemons = [
            self.cleaned_data['pokemon_1'].lower().strip(),
            self.cleaned_data['pokemon_2'].lower().strip(),
            self.cleaned_data['pokemon_3'].lower().strip()
        ]

        if not is_pokemons_sum_valid(pokemons):
            raise forms.ValidationError(
                'Trainer, your pokemon team stats can not sum more than 600 points.'
            )

        return cleaned_data

    def save(self, commit=True):
        pokemons = [
            self.cleaned_data['pokemon_1'].lower().strip(),
            self.cleaned_data['pokemon_2'].lower().strip(),
            self.cleaned_data['pokemon_3'].lower().strip()
        ]
        self.instance.save()

        for pokemon in pokemons:
            if Pokemon.objects.filter(name=pokemon).count() == 0:
                Pokemon.objects.create(
                    name=pokemon,
                    attack=get_pokemon_stats(pokemon)['attack'],
                    defense=get_pokemon_stats(pokemon)['defense'],
                    hitpoints=get_pokemon_stats(pokemon)['hitpoints'],
                )

        return super().save()
