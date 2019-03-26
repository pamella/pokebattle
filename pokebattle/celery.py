# coding: utf-8
# pylint: skip-file

from __future__ import absolute_import

import os

from django.apps import apps

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokebattle.settings.local")

app = Celery('pokebattle_tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

app.conf.beat_schedule = {
    'save_pokeapi_pokemons': {
        'task': 'pokemons.tasks.task_save_pokeapi_pokemons',
        'schedule': crontab(day_of_week='wed', hour='11', minute='0'),
    }
}
