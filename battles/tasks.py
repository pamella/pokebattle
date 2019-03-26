import logging

from battles.helpers.fight import run_battle
from battles.models import Battle
from pokebattle import celery_app


@celery_app.task
def task_run_battles(battle_id):
    logging.info('run battles')
    battle = Battle.objects.get(id=battle_id)
    run_battle(battle)
