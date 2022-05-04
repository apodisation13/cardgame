from django.core.management.base import BaseCommand
from pyexcel_odsr import get_data

from apps.cards.models import Card


class Command(BaseCommand):
    help = 'upload images'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        data = get_data("database.ods")

        # ЗАГРУЗКА cards.Card
        cards_cards = data["Cards.Card"]

        cards = Card.objects.order_by('pk').all()
        i = 1
        for c in cards:
            c.image = cards_cards[i][11]
            c.save()
            i += 1
