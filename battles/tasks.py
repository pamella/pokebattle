from celery.utils.log import get_task_logger

from battles.helpers.fight import run_battle
from battles.models import Battle
from pokebattle import celery_app


logger = get_task_logger(__name__)


@celery_app.task
def task_run_battles(battle_id):
    logger.info('Task: Running battle %d', (battle_id))
    battle = Battle.objects.get(id=battle_id)
    run_battle(battle)
