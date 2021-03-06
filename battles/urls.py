# URLs de battles
from django.urls import path
from django.views.generic.base import TemplateView

from battles.views import (
    BattlesListView, CreateBattleView, DetailBattleView, InviteFriendView, PokemonAutocompleteView,
    SelectTrainerTeamView
)


app_name = 'battles'

urlpatterns = [
    path('my_battles/', BattlesListView.as_view(), name='list_battle'),
    path('create_battle/', CreateBattleView.as_view(), name='create_battle'),
    path('select_team/', SelectTrainerTeamView.as_view(), name='select_team'),
    path('success/', TemplateView.as_view(template_name='battles/success.html'), name='success'),
    path('detail/<int:pk>/', DetailBattleView.as_view(), name='detail_battle'),
    path('pokemon_autocomplete/', PokemonAutocompleteView.as_view(), name='pokemon_autocomplete'),
    path('invite_friend/', InviteFriendView.as_view(), name='invite_friend'),

]
