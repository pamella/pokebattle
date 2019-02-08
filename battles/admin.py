from django.contrib import admin

from battles.models import Battle, TrainerTeam


class BattleAdmin(admin.ModelAdmin):
    list_display = ('trainer_opponent', )


admin.site.register(Battle, BattleAdmin)
admin.site.register(TrainerTeam)
