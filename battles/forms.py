from django import forms

from battles.helpers.form import TeamBaseForm
from battles.models import Battle, Invite, TrainerTeam
from users.models import User


class CreateBattleForm(TeamBaseForm):
    class Meta:
        model = Battle
        fields = ('trainer_opponent', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.exclude(id=self.initial['trainer_creator'].id)
        self.fields['trainer_opponent'].queryset = users


class SelectTrainerTeamForm(TeamBaseForm):
    class Meta:
        model = TrainerTeam
        fields = ('pokemon_1', 'pokemon_2', 'pokemon_3')


class InviteFriendForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('invited', )

    def clean(self):
        cleaned_data = super().clean()
        invited_email = self.cleaned_data['invited']
        if User.objects.filter(email=invited_email):
            raise forms.ValidationError(
                "This user is already a member of Pokebattle team!"
            )
        for invite in Invite.objects.all():
            if invite.invited == invited_email:
                raise forms.ValidationError(
                    "This user email has already been invited to PokeBattle!"
                )
        return cleaned_data
