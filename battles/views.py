from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from battles.forms import CreateBattleForm
from battles.models import Battle


class CreateBattleView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):  # pylint: disable=too-many-ancestors
    template_name = "battles/create_battle.html"
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
