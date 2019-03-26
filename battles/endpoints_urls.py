from django.conf.urls import url

from battles.endpoints import DetailBattleEndpoint


urlpatterns = [
    url(r'^battle/(?P<pk>[\w-]+)$', DetailBattleEndpoint.as_view(), name='detail_battle_endpoint'),

]
