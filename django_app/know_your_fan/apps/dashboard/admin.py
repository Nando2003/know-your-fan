from django.contrib import admin
from apps.dashboard.models.team_model import Team
from apps.dashboard.models.game_model import Game

admin.site.register(Team)
admin.site.register(Game)
