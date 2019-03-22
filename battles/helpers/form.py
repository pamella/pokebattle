from collections import Counter

from django import forms

from dal import autocomplete

from battles.choices import POKEMON_ORDER_CHOICES
from battles.helpers.fight import order_battle_pokemons
from pokemons.helpers import is_pokemons_sum_valid
from pokemons.models import Pokemon


class TeamBaseForm(forms.ModelForm):
    pokemon_1 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='battles:pokemon_autocomplete',
            attrs={
                'data-placeholder': 'Autocomplete pokemon name...',
                'data-minimum-input-length': 3,
                'data-html': True,
            },
        )
    )
    pokemon_2 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='battles:pokemon_autocomplete',
            attrs={
                'data-placeholder': 'Autocomplete pokemon name...',
                'data-minimum-input-length': 3,
                'data-html': True,
            },
        )
    )
    pokemon_3 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='battles:pokemon_autocomplete',
            attrs={
                'data-placeholder': 'Autocomplete pokemon name...',
                'data-minimum-input-length': 3,
                'data-html': True,
            },
        )
    )
    order_1 = forms.ChoiceField(choices=POKEMON_ORDER_CHOICES, initial=0, required=True)
    order_2 = forms.ChoiceField(choices=POKEMON_ORDER_CHOICES, initial=1, required=True)
    order_3 = forms.ChoiceField(choices=POKEMON_ORDER_CHOICES, initial=2, required=True)

    def clean(self):
        cleaned_data = super().clean()
        rounds = [
            int(self.cleaned_data['order_1']),
            int(self.cleaned_data['order_2']),
            int(self.cleaned_data['order_3']),
        ]
        if len(Counter(rounds)) != 3:
            raise forms.ValidationError(
                'Trainer, select a different value for each round field.'
            )

        pokemons = order_battle_pokemons(self.cleaned_data)
        if not is_pokemons_sum_valid(pokemons):
            raise forms.ValidationError(
                'Trainer, your pokemon team stats can not sum more than 600 points.'
            )
        return cleaned_data
