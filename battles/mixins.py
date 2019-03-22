from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

from battles.models import Battle


class TrainerIsNotOpponentMixin(UserPassesTestMixin):
    permission_denied_message = "User, you've already select your team."
    redirect_field_name = None

    def test_func(self):
        user = self.request.user
        battle_id = self.request.GET.get('id')
        battle = Battle.objects.get(id=battle_id)
        if (battle.trainer_opponent != user or battle.status == 'SETTLED'):
            return False
        return True

    def handle_no_permission(self):
        return redirect('users:logout')
