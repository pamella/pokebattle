# URLs de battles
from django.conf.urls import url  # noqa

from battles.views import CreateBattleView


app_name = 'battles'

urlpatterns = [
    url(r'^create_battle/', CreateBattleView.as_view(), name='create_battle'),
]
