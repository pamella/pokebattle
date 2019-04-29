from django.urls import reverse

from model_mommy import mommy
from rest_framework import status

from battles.tests.tests_helpers import PokeBattleAPITestCase


class DetailBattleEndpointTest(PokeBattleAPITestCase):
    def test_auth_get_success(self):
        battle = mommy.make('battles.Battle', trainer_creator=self.user)
        response = self.auth_client.get(
            reverse('api_battles:detail_battle_endpoint', kwargs={'pk': battle.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_forbids_user_not_in_battle(self):
        battle = mommy.make('battles.Battle')
        response = self.auth_client.get(
            reverse('api_battles:detail_battle_endpoint', kwargs={'pk': battle.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_correct_object(self):
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
        response = self.auth_client.get(
            reverse('api_battles:detail_battle_endpoint', kwargs={'pk': battle.id}))
        expected_response = {
            "id": battle.id,
            "status": str(battle.status),
            "trainer_creator_id": battle.trainer_creator.id,
            "trainer_creator_email": battle.trainer_creator.email,
            "trainer_opponent_id": battle.trainer_opponent.id,
            "trainer_opponent_email": battle.trainer_opponent.email,
            "trainer_winner_id": None,
            "trainer_winner_email": None,
            "rounds": [
                {
                    "creator_pokemon": {
                        "id": trainer_team_creator.pokemon_1.id,
                        "api_id": trainer_team_creator.pokemon_1.api_id,
                        "name": trainer_team_creator.pokemon_1.name,
                        "sprite": trainer_team_creator.pokemon_1.sprite,
                        "attack": trainer_team_creator.pokemon_1.attack,
                        "defense": trainer_team_creator.pokemon_1.defense,
                        "hitpoints": trainer_team_creator.pokemon_1.hitpoints,
                        "value": trainer_team_creator.pokemon_1.id,
                        "label": trainer_team_creator.pokemon_1.name,
                    },
                    "opponent_pokemon": {
                        "id": trainer_team_opponent.pokemon_1.id,
                        "api_id": trainer_team_opponent.pokemon_1.api_id,
                        "name": trainer_team_opponent.pokemon_1.name,
                        "sprite": trainer_team_opponent.pokemon_1.sprite,
                        "attack": trainer_team_opponent.pokemon_1.attack,
                        "defense": trainer_team_opponent.pokemon_1.defense,
                        "hitpoints": trainer_team_opponent.pokemon_1.hitpoints,
                        "value": trainer_team_opponent.pokemon_1.id,
                        "label": trainer_team_opponent.pokemon_1.name,
                    }
                },
                {
                    "creator_pokemon": {
                        "id": trainer_team_creator.pokemon_2.id,
                        "api_id": trainer_team_creator.pokemon_2.api_id,
                        "name": trainer_team_creator.pokemon_2.name,
                        "sprite": trainer_team_creator.pokemon_2.sprite,
                        "attack": trainer_team_creator.pokemon_2.attack,
                        "defense": trainer_team_creator.pokemon_2.defense,
                        "hitpoints": trainer_team_creator.pokemon_2.hitpoints,
                        "value": trainer_team_creator.pokemon_2.id,
                        "label": trainer_team_creator.pokemon_2.name,
                    },
                    "opponent_pokemon": {
                        "id": trainer_team_opponent.pokemon_2.id,
                        "api_id": trainer_team_opponent.pokemon_2.api_id,
                        "name": trainer_team_opponent.pokemon_2.name,
                        "sprite": trainer_team_opponent.pokemon_2.sprite,
                        "attack": trainer_team_opponent.pokemon_2.attack,
                        "defense": trainer_team_opponent.pokemon_2.defense,
                        "hitpoints": trainer_team_opponent.pokemon_2.hitpoints,
                        "value": trainer_team_opponent.pokemon_2.id,
                        "label": trainer_team_opponent.pokemon_2.name,
                    }
                },
                {
                    "creator_pokemon": {
                        "id": trainer_team_creator.pokemon_3.id,
                        "api_id": trainer_team_creator.pokemon_3.api_id,
                        "name": trainer_team_creator.pokemon_3.name,
                        "sprite": trainer_team_creator.pokemon_3.sprite,
                        "attack": trainer_team_creator.pokemon_3.attack,
                        "defense": trainer_team_creator.pokemon_3.defense,
                        "hitpoints": trainer_team_creator.pokemon_3.hitpoints,
                        "value": trainer_team_creator.pokemon_3.id,
                        "label": trainer_team_creator.pokemon_3.name,
                    },
                    "opponent_pokemon": {
                        "id": trainer_team_opponent.pokemon_3.id,
                        "api_id": trainer_team_opponent.pokemon_3.api_id,
                        "name": trainer_team_opponent.pokemon_3.name,
                        "sprite": trainer_team_opponent.pokemon_3.sprite,
                        "attack": trainer_team_opponent.pokemon_3.attack,
                        "defense": trainer_team_opponent.pokemon_3.defense,
                        "hitpoints": trainer_team_opponent.pokemon_3.hitpoints,
                        "value": trainer_team_opponent.pokemon_3.id,
                        "label": trainer_team_opponent.pokemon_3.name,
                    }
                }
            ]
        }
        self.assertEqual(response.data, expected_response)
