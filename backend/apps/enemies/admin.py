from django.contrib import admin

from apps.enemies.models import Enemy, EnemyLeader, EnemyLeaderAbility, EnemyPassiveAbility, Level, LevelEnemy, Move

admin.site.register(Move)
admin.site.register(EnemyLeaderAbility)
admin.site.register(EnemyPassiveAbility)


@admin.register(EnemyLeader)
class EnemyLeaderAdmin(admin.ModelAdmin):
    model = EnemyLeader
    list_filter = ("faction_id", "ability_id", "passive")
    list_display = [field.name for field in EnemyLeader._meta.fields]
    list_display_links = [field.name for field in EnemyLeader._meta.fields]


@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    model = Enemy
    list_filter = ("faction_id", "color_id", "move_id", "passive", "passive_ability_id")
    list_display = [field.name for field in Enemy._meta.fields]
    list_display_links = [field.name for field in Enemy._meta.fields]


class LevelEnemyInLine(admin.TabularInline):
    model = LevelEnemy


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    inlines = [LevelEnemyInLine, ]
    list_filter = ("difficulty", "enemy_leader_id")
    list_display = ("id", "name", "starting_enemies_number", "difficulty", "number_of_enemies", "enemy_leader")
    list_display_links = ("id", "name", "starting_enemies_number", "difficulty", "number_of_enemies", "enemy_leader")
