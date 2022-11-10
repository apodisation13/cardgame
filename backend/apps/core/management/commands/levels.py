from django.core.management.base import BaseCommand
from django.db import transaction
from pyexcel_odsr import get_data

from apps.enemies.models import Level, LevelEnemy, LevelRelatedLevels


# Загрузка enemies.Level
def enemies_levels(self, data):
    levels = data["Enemies.Level"]
    # print(enemies_levels)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем enemies.Level'))

        last = Level.objects.all().count()

        for line in levels[last + 1:]:
            if line:
                try:
                    Level.objects.create(
                        name=line[1],
                        starting_enemies_number=line[2],
                        difficulty=line[3],
                        enemy_leader_id=line[4],
                        unlocked=line[5],
                        season_id=line[6],
                        x=line[7],
                        y=line[8],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------


# Загрузка enemies.LevelEnemy
def enemies_levelenemy(self, data):
    levelenemy = data["Enemies.LevelEnemy"]
    # print(levelenemy)

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем enemies.LevelEnemy'))

        last = LevelEnemy.objects.all().count()

        for line in levelenemy[last + 1:]:
            if line:
                try:
                    LevelEnemy.objects.create(
                        level_id=line[1],
                        enemy_id=line[2],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))


# Загрузка enemies.LevelRelatedLevels, какие уровни открывают какие!
def enemies_levelrelatedlevels(self, data):
    related_levels = data["Enemies.LevelRelatedLevel"]

    with transaction.atomic():
        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем enemies.LevelRelatedLevels'))

        last = LevelRelatedLevels.objects.all().count()

        for line in related_levels[last + 1:]:
            if line:
                try:
                    LevelRelatedLevels.objects.create(
                        level_id=line[1],
                        related_level_id=line[2],
                        line=line[3] if line[3] != "NULL" else None,
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

        enemies_levels(self, data)
        enemies_levelenemy(self, data)
        enemies_levelrelatedlevels(self, data)
