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
                        ability_id=line[3] if line[3] != "NULL" else None,
                        hp=line[4],
                        base_hp=line[5],
                        has_passive=line[6],
                        passive_ability_id=line[7] if line[7] != "NULL" else None,
                        image=line[8],
                        value=line[9],
                        timer=line[10],
                        default_timer=line[11],
                        reset_timer=line[12],
                        each_tick=line[13],
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
                        has_passive_in_field=line[11],
                        has_passive_in_deck=line[12],
                        has_passive_in_grave=line[13],
                        passive_ability_id=line[14] if line[14] != "NULL" else None,
                        value=line[15],
                        timer=line[16],
                        default_timer=line[17],
                        reset_timer=line[18],
                        each_tick=line[19],
                        has_deathwish=line[20],
                        deathwish_id=line[21] if line[21] != "NULL" else None,
                        deathwish_value=line[22],
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
