import logging

from pokebattle import celery_app
from pokemons.helpers import save_pokeapi_pokemons


@celery_app.task
def task_save_pokeapi_pokemons():
    logging.info('save pokemons from pokapi')
    save_pokeapi_pokemons()
