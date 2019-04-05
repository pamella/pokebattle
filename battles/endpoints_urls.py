from django.conf.urls import url

from battles.endpoints import DetailBattleEndpoint, ListBattleEndpoint


app_name = 'battles'

urlpatterns = [
    url(r'^battle/(?P<pk>[\w-]+)/$', DetailBattleEndpoint.as_view(), name='detail_battle_endpoint'),
    url(r'^my_battles/$', ListBattleEndpoint.as_view(), name='list_battle_endpoint'),

]
