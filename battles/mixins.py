from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

from battles.models import Battle


class TrainerIsNotOpponentMixin(UserPassesTestMixin):
    permission_denied_message = "User, you've already select your team."
    redirect_field_name = None

    def test_func(self):
        battle_id = self.request.GET.get('id')
        trainer_creator = Battle.objects.get(id=battle_id).trainer_creator
        user = self.request.user
        if trainer_creator == user:
            return False
        return True

    def handle_no_permission(self):
        return redirect('users:logout')
