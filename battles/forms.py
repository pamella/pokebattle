from django import forms

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
        
    def save(self):
        pkm1_content = self.cleaned_data['pkm1']
        pkm2_content = self.cleaned_data['pkm2']
        pkm3_content = self.cleaned_data['pkm3']
        self.instance.save()
        TrainerTeam.objects.create(
            trainer=self.initial['user'],
            pokemon_1=Pokemon.objects.get(name=pkm1_content),
            pokemon_2=Pokemon.objects.get(name=pkm2_content),
            pokemon_3=Pokemon.objects.get(name=pkm3_content),
            battle_related=self.instance,
        )
        return super().save()
