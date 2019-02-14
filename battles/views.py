# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from battles.forms import CreateBattleForm
from battles.models import Battle


class CreateBattleView(LoginRequiredMixin, CreateView):     # pylint: disable=too-many-ancestors
    template_name = "battles/create_battle.html"
    success_url = "/"
    model = Battle
    form_class = CreateBattleForm

    def get_initial(self):
        return {
            'user': self.request.user
        }
