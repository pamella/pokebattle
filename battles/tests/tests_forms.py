from model_mommy import mommy

from battles.forms import CreateBattleForm, SelectTrainerTeamForm
from battles.tests.tests_helpers import PokeBattleTestCase


class CreateBattleFormTest(PokeBattleTestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')

    def test_not_found_pokemon_error(self):
        attr = {
            'initial': {
                'trainer_creator': self.user.id
            },
            'data': {
                'pokemon_1': 'dittossss',
                'pokemon_2': 'ditto',
                'pokemon_3': 'dito'
            }
        }
        form = CreateBattleForm(**attr)
        self.assertFalse(form.is_valid())
        with self.assertRaisesMessage(
                Exception,
                '[\'We couldnt find "dittossss". Please, check if you wrote it correctly.\']'):
            form.clean()

    def test_pokemon_team_sum_invalid(self):
        attr = {
            'initial': {
                'trainer_creator': self.user,
            },
            'data': {
                'trainer_opponent': mommy.make('users.User'),
                'pokemon_1': 'slowbro',
                'pokemon_2': 'golem',
                'pokemon_3': 'doduo'
            }
        }
        form = CreateBattleForm(**attr)
        self.assertFalse(form.is_valid())
        with self.assertRaisesMessage(
                Exception,
                'Trainer, your pokemon team stats can not sum more than 600 points.'):
            form.clean()


class SelectTrainerTeamFormTest(PokeBattleTestCase):

    def test_not_found_pokemon_error(self):
        attr = {
            'initial': {
                'trainer_creator': self.user.id
            },
            'data': {
                'pokemon_1': 'dittossss',
                'pokemon_2': 'ditto',
                'pokemon_3': 'dito'
            }
        }
        form = SelectTrainerTeamForm(**attr)
        self.assertFalse(form.is_valid())
        with self.assertRaisesMessage(
                Exception,
                '[\'We couldnt find "dittossss". Please, check if you wrote it correctly.\']'):
            form.clean()

    def test_pokemon_team_sum_invalid(self):
        attr = {
            'initial': {
                'trainer_creator': self.user.id
            },
            'data': {
                'trainer_opponent': mommy.make('users.User'),
                'pokemon_1': 'slowbro',
                'pokemon_2': 'golem',
                'pokemon_3': 'doduo'
            }
        }
        form = SelectTrainerTeamForm(**attr)
        self.assertFalse(form.is_valid())
        with self.assertRaisesMessage(
                Exception,
                'Trainer, your pokemon team stats can not sum more than 600 points.'):
            form.clean()
