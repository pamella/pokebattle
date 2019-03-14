from collections import Counter

from django import forms

from dal import autocomplete

from battles.choices import POKEMON_ORDER_CHOICES
from battles.helpers import order_battle_pokemons
from battles.models import Battle, Invite, TrainerTeam
from pokemons.helpers import is_pokemons_sum_valid
from pokemons.models import Pokemon
from users.models import User


class CreateBattleForm(forms.ModelForm):
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

    class Meta:
        model = Battle
        fields = ('trainer_opponent', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.exclude(id=self.initial['trainer_creator'].id)
        self.fields['trainer_opponent'].queryset = users

    def clean(self):
        cleaned_data = super().clean()
        pokemons = order_battle_pokemons(self.cleaned_data)
        rounds = [
            int(self.cleaned_data['order_1']),
            int(self.cleaned_data['order_2']),
            int(self.cleaned_data['order_3']),
        ]

        if not is_pokemons_sum_valid(pokemons):
            raise forms.ValidationError(
                'Trainer, your pokemon team stats can not sum more than 600 points.'
            )
        if len(Counter(rounds)) != 3:
            raise forms.ValidationError(
                'Trainer, select a different value for each round field.'
            )
        return cleaned_data


class SelectTrainerTeamForm(forms.ModelForm):
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

    class Meta:
        model = TrainerTeam
        fields = ('pokemon_1', 'pokemon_2', 'pokemon_3')

    def clean(self):
        cleaned_data = super().clean()
        pokemons = order_battle_pokemons(self.cleaned_data)

        if not is_pokemons_sum_valid(pokemons):
            raise forms.ValidationError(
                'Trainer, your pokemon team stats can not sum more than 600 points.'
            )
        return cleaned_data


class InviteFriendForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('invited', )

    def clean(self):
        cleaned_data = super().clean()
        invited_email = self.cleaned_data['invited']
        for user in User.objects.all():
            if user.email == invited_email:
                raise forms.ValidationError(
                    "This user is already a member of Pokebattle team!"
                )
        for invite in Invite.objects.all():
            if invite.invited == invited_email:
                raise forms.ValidationError(
                    "This user email has already been invited to PokeBattle!"
                )
        return cleaned_data
