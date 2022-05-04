from django.core.management.base import BaseCommand
from pyexcel_odsr import get_data

from apps.cards.models import Card, Leader
from apps.enemies.models import Enemy


class Command(BaseCommand):
    help = 'upload images'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        data = get_data("database.ods")

        # ЗАГРУЗКА изображений карт
        cards_cards = data["Cards.Card"]

        cards = Card.objects.order_by('pk').all()
        i = 1
        for c in cards:
            c.image = cards_cards[i][11]
            c.name = cards_cards[i][1]
            c.save()
            i += 1
        # -----------------------------------------------------------

        # ЗАГРУЗКА изображений лидеров
        cards_leaders = data["Cards.Leader"]

        leaders = Leader.objects.order_by('pk').all()
        i = 1
        for l in leaders:
            l.image = cards_leaders[i][7]
            l.name = cards_leaders[i][1]
            l.save()
            i += 1
        # -----------------------------------------------------------

        # Загрузка изображений врагов
        enemies_enemies = data["Enemies.Enemy"]

        enemies = Enemy.objects.order_by('pk').all()
        i = 1
        for e in enemies:
            e.image = enemies_enemies[i][8]
            e.save()
            i += 1
        # -----------------------------------------------------------
