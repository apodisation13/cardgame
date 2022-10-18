from apps.enemies.models import Enemy, EnemyLeader, Level, LevelEnemy
from django.contrib import admin


@admin.register(EnemyLeader)
class EnemyLeaderAdmin(admin.ModelAdmin):
    model = EnemyLeader
    list_filter = ("faction_id", "ability_id", "has_passive")
    list_display = [field.name for field in EnemyLeader._meta.fields]
    list_display_links = [field.name for field in EnemyLeader._meta.fields]


@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    model = Enemy
    list_filter = ("faction_id", "color_id", "move_id", "has_passive", "passive_ability_id")
    list_display = [field.name for field in Enemy._meta.fields]
    list_display_links = [field.name for field in Enemy._meta.fields]


class LevelEnemyInLine(admin.TabularInline):
    model = LevelEnemy
#
#
# class LevelInline(admin.TabularInline):
#     model = Level


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    inlines = [LevelEnemyInLine, ]
    list_filter = ("difficulty", "enemy_leader_id")
    list_display = ("id", "name", "starting_enemies_number", "difficulty",
                    "number_of_enemies", "enemy_leader", "get_related_levels")
    list_display_links = ("id", "name", "starting_enemies_number",
                          "difficulty", "number_of_enemies",
                          "enemy_leader", "get_related_levels")
