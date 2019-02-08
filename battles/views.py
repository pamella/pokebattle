# from django.shortcuts import render
from django.views.generic.base import TemplateView


class CreateBattleView(TemplateView):
    template_name = "create_battle.html"
