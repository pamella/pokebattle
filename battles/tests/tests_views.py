from django.test import Client, TestCase
from django.urls import reverse

from model_mommy import mommy

from battles.models import Battle


class CreateBattleViewTest(TestCase):

    def setUp(self):
        self._user_password = '123456'
        self.user = mommy.prepare('users.User', email='user@email.com')
        self.user.set_password(self._user_password)
        self.user.save()
        self.auth_client = Client()
        self.auth_client.login(email=self.user.email, password=self._user_password)
        self.view_url = reverse('battles:create_battle')
        self.battle = mommy.make('battles.Battle')
        self.battle_attr = {
            'id': self.battle.id,
            'trainer_creator': self.battle.trainer_creator.id,
            'trainer_opponent': self.battle.trainer_opponent.id
        }

    def test_auth_get_success(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_not_auth_login_redirect(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, expected_url='/login/?next=/create_battle/')

    def test_battle_creation_in_db(self):
        response = self.client.post(self.view_url, self.battle_attr)
        battle = Battle.objects.filter(id=self.battle.id).exists()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(battle)


class SelectTrainerTeamTest(TestCase):
    def setUp(self):
        self._user_password = '123456'
        self.user = mommy.prepare('users.User', email='user@email.com')
        self.user.set_password(self._user_password)
        self.user.save()
        self.auth_client = Client()
        self.auth_client.login(email=self.user.email, password=self._user_password)
        self.view_url = reverse('battles:select_team')

    def test_auth_get_success(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_not_auth_login_redirect(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, expected_url='/login/?next=/select_team/')


class BattlesListViewTest(TestCase):
    def setUp(self):
        self._user_password = '123456'
        self.user = mommy.prepare('users.User', email='user@email.com')
        self.user.set_password(self._user_password)
        self.user.save()
        self.auth_client = Client()
        self.auth_client.login(email=self.user.email, password=self._user_password)
        self.view_url = reverse('battles:list_battle')

    def test_auth_get_success(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_not_auth_login_redirect(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, expected_url='/login/?next=/my_battles/')
