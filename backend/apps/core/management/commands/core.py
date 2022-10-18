from django.core.management.base import BaseCommand
from pyexcel_odsr import get_data

from apps.core.models import (
    Ability,
    Color,
    EnemyLeaderAbility,
    EnemyPassiveAbility,
    Faction,
    Move,
    PassiveAbility,
    Type,
)


class Command(BaseCommand):
    help = 'core.Factions, core.Colors'

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

        # ЗАГРУЗКА core.Faction
        factions = data["Faction"]
        # print(factions)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardFaction'))
        for line in factions[1:]:
            if line:
                try:
                    Faction.objects.create(
                        name=line[1]
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # Загрузка core.Color
        colors = data["Color"]
        # print(colors)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardColor'))
        for line in colors[1:]:
            if line:
                try:
                    Color.objects.create(
                        name=line[1]
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # Загрузка cards.Type
        card_types = data["Type"]
        # print(card_types)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardType'))
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
        cards_ability = data["Ability"]
        # print(cards_ability)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardAbility'))
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

        # ЗАГРУЗКА CardPassiveAbility
        cards_passive_ability = data["CardPassiveAbility"]
        # print(cards_ability)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardPassiveAbility'))
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

        # Загрузка enemies.Move
        enemies_moves = data["Move"]
        # print(enemies_moves)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyMove'))
        for line in enemies_moves[1:]:
            if line:
                try:
                    Move.objects.create(
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

        # Загрузка enemies.EnemyPassiveAbility
        enemies_enemy_passive_abilities = data["EnemyPassiveAbility"]
        # print(enemies_enemy_passive_abilities)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyPassiveAbility'))
        for line in enemies_enemy_passive_abilities[1:]:
            if line:
                try:
                    EnemyPassiveAbility.objects.create(
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

        # Загрузка enemies.EnemyLeaderAbility
        enemies_enemy_leader_abilities = data["EnemyLeaderAbility"]
        # print(enemies_enemy_leader_abilities)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyLeaderAbility'))
        for line in enemies_enemy_leader_abilities[1:]:
            if line:
                try:
                    EnemyLeaderAbility.objects.create(
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
