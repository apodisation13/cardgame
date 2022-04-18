from django.core.management.base import BaseCommand
from pyexcel_odsr import get_data

from apps.cards.models import Ability, Card, CardDeck, Deck, Leader, PassiveAbility, Type


class Command(BaseCommand):
    help = 'cards: Types, Abilities, Leaders, Cards, Decks(base-deck)+CardDeck'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        data = get_data("database.ods")

        # Загрузка cards.Type
        card_types = data["Cards.Type"]
        # print(card_types)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.Type'))
        for line in card_types[1:]:
            if line:
                try:
                    Type.objects.create(
                        name=line[1]
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # ЗАГРУЗКА cards.Ability
        cards_ability = data["Cards.Ability"]
        # print(cards_ability)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.Ability'))
        for line in cards_ability[1:]:
            if line:
                try:
                    Ability.objects.create(
                        name=line[1],
                        description=line[2],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # ЗАГРУЗКА cards.PassiveAbility
        cards_passive_ability = data["Cards.PassiveAbility"]
        # print(cards_ability)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.PassiveAbility'))
        for line in cards_passive_ability[1:]:
            if line:
                try:
                    PassiveAbility.objects.create(
                        name=line[1],
                        description=line[2],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # ЗАГРУЗКА cards.Leader
        cards_leaders = data["Cards.Leader"]
        # print(cards_leaders)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.Leader'))
        for line in cards_leaders[1:]:
            if line:
                try:
                    p_l_a_id = line[8]
                    if p_l_a_id != "NULL":
                        Leader.objects.create(
                            name=line[1],
                            locked=line[2],
                            faction_id=line[3],
                            ability_id=line[4],
                            damage=line[5],
                            charges=line[6],
                            image=line[7],
                            has_passive=line[8],
                            passive_ability_id=p_l_a_id,
                        )
                        success += 1
                    else:
                        Leader.objects.create(
                            name=line[1],
                            locked=line[2],
                            faction_id=line[3],
                            ability_id=line[4],
                            damage=line[5],
                            charges=line[6],
                            image=line[7],
                            has_passive=line[8],
                        )
                        success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # ЗАГРУЗКА cards.Card
        cards_cards = data["Cards.Card"]
        # print(cards_cards)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.Card'))
        for line in cards_cards[1:]:
            if line:
                try:
                    passive_card_ability_id = line[12]
                    if passive_card_ability_id != "NULL":
                        Card.objects.create(
                            name=line[1],
                            locked=line[2],
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
                            passive_ability_id=passive_card_ability_id
                        )
                        success += 1
                    else:
                        Card.objects.create(
                            name=line[1],
                            locked=line[2],
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
                        )
                        success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # ЗАГРУЗКА cards.Deck (base-deck)
        cards_deck = data["Cards.Deck"]
        # print(cards_deck)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.Deck'))
        for line in cards_deck[1:]:
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
        # -----------------------------------------------------------

        # ЗАГРУЗКА cards.CardDeck (for base-deck)
        cards_carddeck = data["Cards.CardDeck"]
        # print(cards_carddeck)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем cards.CardDeck'))
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
        # -----------------------------------------------------------
