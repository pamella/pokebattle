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
                'pokemon_1': mommy.make(
                    'pokemons.Pokemon', name='dittossss').id,
                'pokemon_2': mommy.make(
                    'pokemons.Pokemon', name='abra').id,
                'pokemon_3': mommy.make(
                    'pokemons.Pokemon', name='arbok').id,
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
                'pokemon_1': mommy.make(
                    'pokemons.Pokemon', name='slowbro').id,
                'pokemon_2': mommy.make(
                    'pokemons.Pokemon', name='golem').id,
                'pokemon_3': mommy.make(
                    'pokemons.Pokemon', name='doduo').id,
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
                'pokemon_1': mommy.make(
                    'pokemons.Pokemon', name='dittossss').id,
                'pokemon_2': mommy.make(
                    'pokemons.Pokemon', name='abra').id,
                'pokemon_3': mommy.make(
                    'pokemons.Pokemon', name='arbok').id,
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
                'pokemon_1': mommy.make(
                    'pokemons.Pokemon', name='slowbro').id,
                'pokemon_2': mommy.make(
                    'pokemons.Pokemon', name='golem').id,
                'pokemon_3': mommy.make(
                    'pokemons.Pokemon', name='doduo').id,
            }
        }
        form = SelectTrainerTeamForm(**attr)
        self.assertFalse(form.is_valid())
        with self.assertRaisesMessage(
                Exception,
                'Trainer, your pokemon team stats can not sum more than 600 points.'):
            form.clean()
