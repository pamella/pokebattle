from celery.utils.log import get_task_logger

from pokebattle import celery_app
from pokemons.helpers import save_pokeapi_pokemons


logger = get_task_logger(__name__)


@celery_app.task
def task_save_pokeapi_pokemons():
    logger.info('Task: Save pokemons from PokeAPI')
    save_pokeapi_pokemons()
