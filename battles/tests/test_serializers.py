from model_mommy import mommy

from battles.serializers import BattleReadSerializer
from battles.tests.tests_helpers import PokeBattleTestCase


class BattleReadSerializerTest(PokeBattleTestCase):
    def test_has_correct_keys(self):
        battle = mommy.make('battles.Battle', trainer_creator=self.user)
        serializer = BattleReadSerializer(battle)
        expected_keys = [
            'id',
            'trainer_creator_id', 'trainer_creator_email',
            'trainer_opponent_id', 'trainer_opponent_email',
            'trainer_winner_id', 'trainer_winner_email',
            'rounds',
        ]
        self.assertCountEqual(serializer.data.keys(), expected_keys)

    def test_rounds_return(self):
        battle = mommy.make('battles.Battle', trainer_creator=self.user)
        trainer_team_creator = mommy.make(
            'battles.TrainerTeam',
            battle_related=battle,
            trainer=battle.trainer_creator,
            _fill_optional=['pokemon_1', 'pokemon_2', 'pokemon_3'],
        )
        trainer_team_opponent = mommy.make(
            'battles.TrainerTeam',
            battle_related=battle,
            trainer=battle.trainer_opponent,
            _fill_optional=['pokemon_1', 'pokemon_2', 'pokemon_3'],
        )
        serializer = BattleReadSerializer(battle)
        expected_round1_creator_pokemon = trainer_team_creator.pokemon_1.id
        expected_round2_creator_pokemon = trainer_team_creator.pokemon_2.id
        expected_round3_creator_pokemon = trainer_team_creator.pokemon_3.id
        expected_round1_opponent_pokemon = trainer_team_opponent.pokemon_1.id
        expected_round2_opponent_pokemon = trainer_team_opponent.pokemon_2.id
        expected_round3_opponent_pokemon = trainer_team_opponent.pokemon_3.id
        rounds = serializer.data['rounds']

        self.assertEqual(rounds[0]['creator_pokemon']['id'], expected_round1_creator_pokemon)
        self.assertEqual(rounds[1]['creator_pokemon']['id'], expected_round2_creator_pokemon)
        self.assertEqual(rounds[2]['creator_pokemon']['id'], expected_round3_creator_pokemon)
        self.assertEqual(rounds[0]['opponent_pokemon']['id'], expected_round1_opponent_pokemon)
        self.assertEqual(rounds[1]['opponent_pokemon']['id'], expected_round2_opponent_pokemon)
        self.assertEqual(rounds[2]['opponent_pokemon']['id'], expected_round3_opponent_pokemon)
