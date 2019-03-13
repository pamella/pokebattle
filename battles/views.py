from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.utils.html import format_html
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from dal import autocomplete

from battles.forms import CreateBattleForm, InviteFriendForm, SelectTrainerTeamForm
from battles.helpers import send_invited_friend_email
from battles.models import Battle, Invite, TrainerTeam
from pokemons.helpers import get_pokemons_from_trainerteam
from pokemons.models import Pokemon


class CreateBattleView(
        LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
            trainer=self.request.user.get_short_name(),
        )


class SelectTrainerTeam(
        LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
            trainer=self.request.user.get_short_name(),
        )


class BattlesListView(LoginRequiredMixin, ListView):
    template_name = 'battles/list_battle.html'
    model = Battle

    def get_context_data(self, **kwargs):   # pylint: disable=arguments-differ
        context = super().get_context_data(**kwargs)
        context['on_going'] = Battle.objects.filter(status='ON_GOING')
        context['settled'] = Battle.objects.filter(status='SETTLED')
        context['has_battle_before'] = Battle.objects.filter(
            Q(trainer_creator=self.request.user) | Q(trainer_opponent=self.request.user)
        ).exists()
        context['trainer_team'] = TrainerTeam.objects.filter(trainer=self.request.user)

        return context


class DetailBattleView(LoginRequiredMixin, DetailView):
    model = Battle
    template_name = 'battles/detail_battle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemons_creator = get_pokemons_from_trainerteam(
            self.object.id, self.object.trainer_creator)
        pokemons_opponent = get_pokemons_from_trainerteam(
            self.object.id, self.object.trainer_opponent)
        context['pokemons'] = zip(pokemons_creator, pokemons_opponent)
        return context


class PokemonAutocompleteView(
        LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_result_label(self, result):
        return format_html('<img src="{}"> {}', result.sprite, result.name)

    def get_selected_result_label(self, result):
        return result.name

    def get_queryset(self):
        qs = Pokemon.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class InviteFriendView(
        LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Invite
    template_name = 'battles/invite_friend.html'
    form_class = InviteFriendForm
    success_url = '/success/'
    success_message = '%(user)s, your friend was successfully invited!'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            user=self.request.user.get_short_name(),
        )

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.inviter = self.request.user
        self.instance.save()
        # send email to invited friend
        send_invited_friend_email(self.instance)
        return super().form_valid(form)
