from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from battles.forms import CreateBattleForm, SelectTrainerTeamForm
from battles.models import Battle, TrainerTeam


class CreateBattleView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):  # pylint: disable=too-many-ancestors
    template_name = 'battles/create_battle.html'
    model = Battle
    form_class = CreateBattleForm
    success_url = '/success/'
    success_message = '%(trainer)s, your challenge was successfully submitted!'

    def get_initial(self):
        return {
            'user': self.request.user
        }

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            trainer=self.request.user,
        )


class SelectTrainerTeam(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):  # pylint: disable=too-many-ancestors
    template_name = 'battles/select_team.html'
    model = TrainerTeam
    form_class = SelectTrainerTeamForm
    success_url = '/success/'
    success_message = '%(trainer)s, your team was successfully submitted to battle!'

    def get_initial(self):
        return {
            'user': self.request.user,
            'battle': self.request.GET.get('id')
        }

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            trainer=self.request.user,
        )


class BattlesListView(ListView):  # pylint: disable=too-many-ancestors
    template_name = 'battles/list_battle.html'
    model = Battle

    def get_queryset(self):
        return Battle.objects.filter(trainer_opponent=self.request.user.id)
