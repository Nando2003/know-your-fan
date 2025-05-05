from django.core.management.base import BaseCommand
from apps.dashboard.models.game_model import Game

class Command(BaseCommand):
    help = "Popula os jogos padrão (CS2, VALORANT, LOL)"

    def handle(self, *args, **kwargs):
        games = ["CS2", "VALORANT", "LOL"]
        for name in games:
            obj, created = Game.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Jogo '{name}' criado."))
            else:
                self.stdout.write(self.style.WARNING(f"Jogo '{name}' já existia."))
                