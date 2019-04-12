from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.utils.html import format_html
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from dal import autocomplete

from battles.forms import CreateBattleForm, InviteFriendForm, SelectTrainerTeamForm
from battles.helpers.email import send_battle_match_invite_email, send_invited_friend_email
from battles.helpers.fight import order_battle_pokemons
from battles.mixins import TrainerIsNotOpponentMixin
from battles.models import Battle, Invite, TrainerTeam
from battles.tasks import task_run_battles
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
            'trainer_creator': self.request.user
        }

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            trainer=self.request.user.get_short_name(),
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.trainer_creator = self.request.user
        self.object.status = 'ON_GOING'
        pokemons = order_battle_pokemons(form.cleaned_data)
        self.object.save()
        TrainerTeam.objects.create(
            trainer=self.request.user,
            pokemon_1=Pokemon.objects.get(name=pokemons[0]),
            pokemon_2=Pokemon.objects.get(name=pokemons[1]),
            pokemon_3=Pokemon.objects.get(name=pokemons[2]),
            battle_related=self.object,
        )
        # send battle match invite email to opponent
        send_battle_match_invite_email(self.object)
        return super().form_valid(form)


class SelectTrainerTeamView(
        LoginRequiredMixin, TrainerIsNotOpponentMixin, SuccessMessageMixin,
        CreateView):
    template_name = 'battles/select_team.html'
    model = TrainerTeam
    form_class = SelectTrainerTeamForm
    success_url = '/success/'
    success_message = '%(trainer)s, your team was successfully submitted to battle!'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            trainer=self.request.user.get_short_name(),
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.trainer = self.request.user
        self.object.battle_related = Battle.objects.get(id=self.request.GET.get('id'))
        pokemons = order_battle_pokemons(form.cleaned_data)
        self.object.pokemon_1 = Pokemon.objects.get(name=pokemons[0])
        self.object.pokemon_2 = Pokemon.objects.get(name=pokemons[1])
        self.object.pokemon_3 = Pokemon.objects.get(name=pokemons[2])
        self.object.save()
        # run battle async
        task_run_battles.delay(self.object.battle_related.id)
        return super().form_valid(form)


class BattlesListView(LoginRequiredMixin, ListView):
    # template_name = 'battles/list_battle.html'
    template_name = 'battles/list_battle_react.html'
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
    # template_name = 'battles/detail_battle.html'
    template_name = 'battles/detail_battle_react.html'

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
