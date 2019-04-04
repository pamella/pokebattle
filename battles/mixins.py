from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login

from battles.models import Battle


class TrainerIsNotOpponentMixin(UserPassesTestMixin):
    permission_denied_message = "User, you've already select your team."

    def test_func(self):
        user = self.request.user
        battle_id = self.request.GET.get('id')
        battle = Battle.objects.get(id=battle_id)
        if (battle.trainer_opponent != user or battle.status == 'SETTLED'):
            return False
        return True

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return redirect_to_login(
            self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
