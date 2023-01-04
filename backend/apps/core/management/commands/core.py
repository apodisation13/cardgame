import json

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
    GameConst,
    Move,
    PassiveAbility,
    Type,
)


# ЗАГРУЗКА core.Faction
def core_factions(self, data):
    factions = data["Faction"]

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardFaction'))

        last = Faction.objects.all().count()

        for line in factions[last + 1:]:
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

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardColor'))

        last = Color.objects.all().count()

        for line in colors[last + 1:]:
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

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardType'))

        last = Type.objects.all().count()

        for line in card_types[last + 1:]:
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

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardAbility'))

        last = Ability.objects.all().count()

        for line in cards_ability[last + 1:]:
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

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем CardPassiveAbility'))

        last = PassiveAbility.objects.all().count()

        for line in cards_passive_ability[last + 1:]:
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

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyMove'))

        last = Move.objects.all().count()

        for line in enemies_moves[last + 1:]:
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

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyPassiveAbility'))

        last = EnemyPassiveAbility.objects.all().count()

        for line in enemies_enemy_passive_abilities[last + 1:]:
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

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyLeaderAbility'))

        last = EnemyLeaderAbility.objects.all().count()

        for line in enemies_enemy_leader_abilities[last + 1:]:
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

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем EnemyDeathwish'))

        last = Deathwish.objects.all().count()

        for line in deathwishes[last + 1:]:
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


# Загрузка GameConst
def core_game_const(self, data):
    game_const = data["GameConst"]

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем GameConst'))

        last = GameConst.objects.all().count()

        for line in game_const[last + 1:]:
            if line:
                try:
                    GameConst.objects.create(data=json.loads(line[1]))
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
        core_game_const(self, data)
