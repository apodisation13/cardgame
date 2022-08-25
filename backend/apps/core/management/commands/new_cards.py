from django.core.management.base import BaseCommand
from pyexcel_odsr import get_data

from apps.cards.models import Card


class Command(BaseCommand):
    help = 'upload images'

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

        # ЗАГРУЗКА НОВЫХ КАРТ
        cards_cards = data["Cards.Card"]

        last_card = Card.objects.order_by('pk').last()
        # print(last_card.pk)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем НОВЫЕ КАРТЫ'))
        for line in cards_cards[last_card.pk + 1:]:
            if line:
                try:
                    passive_card_ability_id = line[14]
                    if passive_card_ability_id != "NULL":
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
                            passive_ability_id=passive_card_ability_id,
                            timer=line[15],
                        )
                        success += 1
                    else:
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
                            timer=line[15],
                        )
                        success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------
