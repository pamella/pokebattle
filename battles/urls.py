# URLs de battles
from django.conf.urls import url  # noqa
from django.views.generic.base import TemplateView

from battles.views import BattlesListView, CreateBattleView, SelectTrainerTeam


app_name = 'battles'

urlpatterns = [
    url(r'^my_battles/', BattlesListView.as_view(), name='list_battle'),
    url(r'^create_battle/', CreateBattleView.as_view(), name='create_battle'),
    url(r'^select_team/', SelectTrainerTeam.as_view(), name='select_team'),
    url(r'^success/$', TemplateView.as_view(template_name='battles/success.html'), name='success'),
]
