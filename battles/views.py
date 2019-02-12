# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from battles.forms import CreateBattleForm
from battles.models import Battle, TrainerTeam


class CreateBattleView(LoginRequiredMixin, CreateView):
    template_name = "battles/create_battle.html"
    success_url = "/"
    model = Battle
    form_class = CreateBattleForm

    def get_initial(self):
        return {
            'user': self.request.user
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
