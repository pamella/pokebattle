# URLs de battles
from django.conf.urls import url  # noqa
from django.views.generic.base import TemplateView

from battles.views import CreateBattleView


app_name = 'battles'

urlpatterns = [
    url(r'^create_battle/', CreateBattleView.as_view(), name='create_battle'),
    url(r'^success/$', TemplateView.as_view(template_name='battles/success.html'), name='success'),
]
