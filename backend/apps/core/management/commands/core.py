from django.core.management.base import BaseCommand
from django.db import transaction
from pyexcel_odsr import get_data

from apps.core.models import (
    Ability,
    Color,
    Deathwish,
    EnemyLeaderAbility,
    EnemyPassiveAbility,
    Faction,
    Move,
    PassiveAbility,
    Type,
)


# ЗАГРУЗКА core.Faction
def core_factions(self, data):
    factions = data["Faction"]
    # print(factions)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardFaction'))

        last_faction = Faction.objects.last()
        if last_faction:
            start = last_faction.pk
        else:
            start = 0

        for line in factions[start + 1:]:
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


# Загрузка core.Color
def core_colors(self, data):
    colors = data["Color"]
    # print(colors)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardColor'))

        last_color = Color.objects.last()
        if last_color:
            start = last_color.pk
        else:
            start = 0

        for line in colors[start + 1:]:
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


# Загрузка cards.Type
def core_types(self, data):
    card_types = data["Type"]
    # print(card_types)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardType'))

        last_type = Type.objects.last()
        if last_type:
            start = last_type.pk
        else:
            start = 0

        for line in card_types[start + 1:]:
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


# ЗАГРУЗКА cards.Ability
def core_abilities(self, data):
    cards_ability = data["Ability"]
    # print(cards_ability)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardAbility'))

        last_ability = Ability.objects.last()
        if last_ability:
            start = last_ability.pk
        else:
            start = 0

        for line in cards_ability[start + 1:]:
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


# ЗАГРУЗКА CardPassiveAbility
def core_passive_abilities(self, data):
    cards_passive_ability = data["CardPassiveAbility"]
    # print(cards_ability)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardPassiveAbility'))

        last_pa = PassiveAbility.objects.last()
        if last_pa:
            start = last_pa.pk
        else:
            start = 0

        for line in cards_passive_ability[start + 1:]:
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


# Загрузка enemies.Move
def core_enemies_move(self, data):
    enemies_moves = data["Move"]
    # print(enemies_moves)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyMove'))

        last_move = Move.objects.last()
        if last_move:
            start = last_move.pk
        else:
            start = 0

        for line in enemies_moves[start + 1:]:
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


# Загрузка enemies.EnemyPassiveAbility
def core_enemy_passive_ability(self, data):
    enemies_enemy_passive_abilities = data["EnemyPassiveAbility"]
    # print(enemies_enemy_passive_abilities)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyPassiveAbility'))

        last = EnemyPassiveAbility.objects.last()
        if last:
            start = last.pk
        else:
            start = 0

        for line in enemies_enemy_passive_abilities[start + 1:]:
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


# Загрузка enemies.EnemyLeaderAbility
def core_enemy_leader_ability(self, data):
    enemies_enemy_leader_abilities = data["EnemyLeaderAbility"]
    # print(enemies_enemy_leader_abilities)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyLeaderAbility'))

        last = EnemyLeaderAbility.objects.last()
        if last:
            start = last.pk
        else:
            start = 0

        for line in enemies_enemy_leader_abilities[start + 1:]:
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


# Загрузка enemies.Deathwish
def core_deathwish(self, data):
    deathwishes = data["Deathwish"]
    # print(deathwishes)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyDeathwish'))

        last = Deathwish.objects.last()
        if last:
            start = last.pk
        else:
            start = 0

        for line in deathwishes[start + 1:]:
            if line:
                try:
                    Deathwish.objects.create(
                        name=line[1],
                        description=line[2],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))


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

        core_factions(self, data)
        core_colors(self, data)
        core_types(self, data)
        core_abilities(self, data)
        core_passive_abilities(self, data)
        core_enemies_move(self, data)
        core_enemy_passive_ability(self, data)
        core_enemy_leader_ability(self, data)
        core_deathwish(self, data)
