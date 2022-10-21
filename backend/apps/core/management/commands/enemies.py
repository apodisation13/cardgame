from apps.enemies.models import Enemy, EnemyLeader, Level, LevelEnemy
from django.core.management.base import BaseCommand
from pyexcel_odsr import get_data


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

        # Загрузка enemies.EnemyLeader
        enemies_enemy_leaders = data["Enemies.EnemyLeader"]
        # print(enemies_enemy_leaders)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем enemies.EnemyLeader'))
        for line in enemies_enemy_leaders[1:]:
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
        # -----------------------------------------------------------

        # Загрузка enemies.Enemy
        enemies_enemies = data["Enemies.Enemy"]
        # print(enemies_enemies)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем enemies.Enemy'))
        for line in enemies_enemies[1:]:
            if line:
                try:
                    passive = line[9]
                    if passive == "False":
                        Enemy.objects.create(
                            name=line[1],
                            faction_id=line[2],
                            color_id=line[3],
                            move_id=line[4],
                            damage=line[5],
                            hp=line[6],
                            shield=line[7],
                            image=line[8],
                        )
                        success += 1
                    else:
                        Enemy.objects.create(
                            name=line[1],
                            faction_id=line[2],
                            color_id=line[3],
                            move_id=line[4],
                            damage=line[5],
                            hp=line[6],
                            shield=line[7],
                            image=line[8],
                            has_passive=line[9],
                            passive_ability_id=line[10],
                            passive_increase_damage=line[11],
                            passive_heal=line[12],
                            passive_heal_leader=line[13],
                        )
                        success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # Загрузка enemies.Level
        enemies_levels = data["Enemies.Level"]
        # print(enemies_levels)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем enemies.Level'))
        for line in enemies_levels[1:]:
            if line:
                try:
                    Level.objects.create(
                        name=line[1],
                        starting_enemies_number=line[2],
                        difficulty=line[3],
                        enemy_leader_id=line[4],
                        unlocked=line[5],
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # Загрузка enemies.LevelEnemy
        enemies_levelenemy = data["Enemies.LevelEnemy"]
        # print(enemies_levelenemy)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем enemies.LevelEnemy'))
        for line in enemies_levelenemy[1:]:
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
        # -----------------------------------------------------------
