from django.core.management.base import BaseCommand
from django.db import transaction
from pyexcel_odsr import get_data

from apps.enemies.models import Enemy, EnemyLeader, Season


# Загрузка enemies.EnemyLeader
def enemies_enemy_leader(self, data):
    enemies_enemy_leaders = data["Enemies.EnemyLeader"]
    # print(enemies_enemy_leaders)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем enemies.EnemyLeader'))

        last = EnemyLeader.objects.all().count()

        for line in enemies_enemy_leaders[last + 1:]:
            if line:
                try:
                    EnemyLeader.objects.create(
                        name=line[1],
                        faction_id=line[2],
                        ability_id=line[3],
                        hp=line[4],
                        damage_once=line[5],
                        damage_per_turn=line[6],
                        heal_self_per_turn=line[7],
                        has_passive=line[8],
                        image=line[9],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))


# Загрузка enemies.Enemy
def enemies_enemies(self, data):
    enemies = data["Enemies.Enemy"]
    # print(enemies)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем enemies.Enemy'))

        last = Enemy.objects.all().count()

        for line in enemies[last + 1:]:
            if line:
                try:
                    Enemy.objects.create(
                        name=line[1],
                        faction_id=line[2],
                        color_id=line[3],
                        move_id=line[4],
                        damage=line[5],
                        hp=line[6],
                        base_hp=line[7],
                        shield=line[8],
                        image=line[9],
                        has_passive=line[10],
                        passive_ability_id=line[11] if line[11] != "NULL" else None,
                        value=line[12],
                        timer=line[13],
                        default_timer=line[14],
                        reset_timer=line[15],
                        has_deathwish=line[16],
                        deathwish_id=line[17] if line[17] != "NULL" else None,
                        deathwish_value=line[18],

                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))


# Загрузка enemies.Season
def enemies_seasons(self, data):
    seasons = data["Enemies.Season"]

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем Enemies.Season'))

        last = Season.objects.all().count()

        for line in seasons[last + 1:]:
            if line:
                try:
                    Season.objects.create(
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
    help = 'enemies: Moves, EnemyLeaderAbilities, EnemyLeaders, Enemies, Level+LevelEnemy'

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

        enemies_enemy_leader(self, data)
        enemies_enemies(self, data)
        enemies_seasons(self, data)
