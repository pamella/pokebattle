from django import forms
from django.db.models import Q

from dal import autocomplete

from battles.helpers import (
    get_battle_winner, send_battle_match_invite_email, send_battle_result_email
)
from battles.models import Battle, Invite, TrainerTeam
from pokemons.helpers import get_pokemon_args, is_pokemons_sum_valid, pokemon_exists
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

    class Meta:
        model = Battle
        fields = ('trainer_opponent', 'trainer_creator', 'status')
        widgets = {
            'trainer_creator': forms.HiddenInput(),
            'status': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial_user_id = initial.get('user') and initial.get('user').id
        initial['trainer_creator'] = initial.get('trainer_creator', initial_user_id)
        initial['status'] = initial.get('status', 'ON_GOING')
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        pokemons = [
            self.cleaned_data['pokemon_1'].name,
            self.cleaned_data['pokemon_2'].name,
            self.cleaned_data['pokemon_3'].name,
        ]

        for pokemon in pokemons:
            if not pokemon_exists(pokemon):
                raise forms.ValidationError(
                    f'We couldnt find "{pokemon}". Please, check if you wrote it correctly.'
                )

        if not is_pokemons_sum_valid(pokemons):
            raise forms.ValidationError(
                'Trainer, your pokemon team stats can not sum more than 600 points.'
            )

        return cleaned_data

    def save(self, commit=True):
        pokemons = [
            self.cleaned_data['pokemon_1'].name,
            self.cleaned_data['pokemon_2'].name,
            self.cleaned_data['pokemon_3'].name,
        ]
        self.instance.save()

        for pokemon in pokemons:
            if Pokemon.objects.filter(name=pokemon).count() == 0:
                pokemon_args = get_pokemon_args(pokemon)
                Pokemon.objects.create(
                    api_id=pokemon_args['api_id'],
                    name=pokemon_args['name'],
                    sprite=pokemon_args['sprite'],
                    attack=pokemon_args['attack'],
                    defense=pokemon_args['defense'],
                    hitpoints=pokemon_args['hitpoints'],
                )

        TrainerTeam.objects.create(
            trainer=self.initial['user'],
            pokemon_1=Pokemon.objects.get(name=pokemons[0]),
            pokemon_2=Pokemon.objects.get(name=pokemons[1]),
            pokemon_3=Pokemon.objects.get(name=pokemons[2]),
            battle_related=self.instance,
        )
        # send battle match invite email to opponent
        send_battle_match_invite_email(self.instance)

        return super().save()


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

    class Meta:
        model = TrainerTeam
        fields = ('trainer', 'battle_related')
        widgets = {
            'trainer': forms.HiddenInput(),
            'battle_related': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial_user_id = initial.get('user') and initial.get('user').id
        initial['trainer'] = initial.get('trainer', initial_user_id)
        initial['battle_related'] = initial.get('battle')
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        pokemons = [
            self.cleaned_data['pokemon_1'].name,
            self.cleaned_data['pokemon_2'].name,
            self.cleaned_data['pokemon_3'].name
        ]

        for pokemon in pokemons:
            if not pokemon_exists(pokemon):
                raise forms.ValidationError(
                    f'We couldnt find "{pokemon}". Please, check if you wrote it correctly.'
                )

        if not is_pokemons_sum_valid(pokemons):
            raise forms.ValidationError(
                'Trainer, your pokemon team stats can not sum more than 600 points.'
            )

        return cleaned_data

    def save(self, commit=True):
        pokemons = [
            self.cleaned_data['pokemon_1'].name,
            self.cleaned_data['pokemon_2'].name,
            self.cleaned_data['pokemon_3'].name
        ]

        trainer_creator = Battle.objects.get(id=self.initial['battle']).trainer_creator
        trainer_team_creator = TrainerTeam.objects.get(
            Q(battle_related=self.initial['battle_related']), Q(trainer=trainer_creator)
        )
        pokemons_creator = [
            trainer_team_creator.pokemon_1,
            trainer_team_creator.pokemon_2,
            trainer_team_creator.pokemon_3
        ]

        pokemons_opponent = []
        for pokemon in pokemons:
            if Pokemon.objects.filter(name=pokemon).count() == 0:
                pokemon_args = get_pokemon_args(pokemon)
                Pokemon.objects.create(
                    api_id=pokemon_args['api_id'],
                    name=pokemon_args['name'],
                    sprite=pokemon_args['sprite'],
                    attack=pokemon_args['attack'],
                    defense=pokemon_args['defense'],
                    hitpoints=pokemon_args['hitpoints'],
                )
            pokemons_opponent.append(Pokemon.objects.get(name=pokemon))

        if get_battle_winner(pokemons_creator, pokemons_opponent) == 'creator':
            Battle.objects.filter(id=self.initial['battle']).update(trainer_winner=trainer_creator)
        else:
            Battle.objects.filter(id=self.initial['battle']).update(
                trainer_winner=self.initial['user'])

        Battle.objects.filter(id=self.initial['battle']).update(status='SETTLED')
        self.instance.trainer = self.initial['user']
        self.instance.pokemon_1 = Pokemon.objects.get(name=pokemons[0])
        self.instance.pokemon_2 = Pokemon.objects.get(name=pokemons[1])
        self.instance.pokemon_3 = Pokemon.objects.get(name=pokemons[2])
        self.instance.battle_related = Battle.objects.get(id=self.initial['battle_related'])
        self.instance.save()
        # send both trainers the battle result email
        send_battle_result_email(self.instance.battle_related)

        return super().save()


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
