from django.test import Client, TestCase

from model_mommy import mommy


class PokeBattleTestCase(TestCase):
    def setUp(self):
        self._user_password = '123456'
        self.user = mommy.prepare('users.User', email='user@email.com')
        self.user.set_password(self._user_password)
        self.user.save()
        self.auth_client = Client()
        self.auth_client.login(email=self.user.email, password=self._user_password)
