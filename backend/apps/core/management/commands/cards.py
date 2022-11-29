from django.core.management.base import BaseCommand
from django.db import transaction
from pyexcel_odsr import get_data

from apps.cards.models import Card, CardDeck, Deck, Leader


# ЗАГРУЗКА cards.Leader
def cards_leaders(self, data):
    leaders = data["Cards.Leader"]

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.Leader'))

        last = Leader.objects.all().count()

        for line in leaders[last + 1:]:
            if line:
                try:
                    Leader.objects.create(
                        name=line[1],
                        unlocked=line[2],
                        faction_id=line[3],
                        ability_id=line[4],
                        damage=line[5],
                        charges=line[6],
                        image=line[7],
                        has_passive=line[8],
                        passive_ability_id=line[9] if line[9] != "NULL" else None,
                        value=line[10],
                        timer=line[11],
                        default_timer=line[12],
                        reset_timer=line[13],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))


# ЗАГРУЗКА cards.Card
def cards_cards(self, data):
    cards = data["Cards.Card"]

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.Card'))

        last = Card.objects.all().count()

        for line in cards[last + 1:]:
            if line:
                try:
                    Card.objects.create(
                        name=line[1],
                        unlocked=line[2],
                        faction_id=line[3],
                        color_id=line[4],
                        type_id=line[5],
                        ability_id=line[6],
                        damage=line[7],
                        charges=line[8],
                        hp=line[9],
                        heal=line[10],
                        image=line[11],
                        has_passive=line[12],
                        has_passive_in_hand=line[13],
                        passive_ability_id=line[14] if line[14] != "NULL" else None,
                        value=line[15],
                        timer=line[16],
                        default_timer=line[17],
                        reset_timer=line[18],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))


# ЗАГРУЗКА cards.Deck (base-deck)
def cards_base_deck(self, data):
    deck = data["Cards.Deck"]
    # print(deck)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.Deck'))

        last = Deck.objects.last()
        if last:
            return

        for line in deck[1:]:
            if line:
                try:
                    Deck.objects.create(
                        name=line[1],
                        health=line[2],
                        leader_id=line[3],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))


# ЗАГРУЗКА cards.CardDeck (for base-deck)
def cards_carddeck_base(self, data):
    cards_carddeck = data["Cards.CardDeck"]
    # print(cards_carddeck)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.CardDeck'))

        last = CardDeck.objects.last()
        if last:
            return

        for line in cards_carddeck[1:]:
            if line:
                try:
                    CardDeck.objects.create(
                        deck_id=line[1],
                        card_id=line[2],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))


class Command(BaseCommand):
    help = 'cards: Leaders, Cards, Decks(base-deck)+CardDeck'

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            dest="path",
        )

    def handle(self, *args, **options):
        path = options.get("path")

        if path:
            data = get_data(f"{path}/database.ods")
        else:
            data = get_data("database.ods")

        cards_leaders(self, data)
        cards_cards(self, data)
        cards_base_deck(self, data)
        cards_carddeck_base(self, data)
