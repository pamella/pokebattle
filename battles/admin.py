from django.contrib import admin

from battles.models import Battle, Invite, TrainerTeam


admin.site.register(Battle)
admin.site.register(TrainerTeam)
admin.site.register(Invite)
