from django.contrib import admin

from apps.enemies.models import Enemy, EnemyLeader, Level, LevelEnemy, LevelRelatedLevels, Season


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


class LevelInline(admin.TabularInline):
    model = LevelRelatedLevels
    fk_name = "level"
    fields = ("line", "related_level")


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    inlines = [LevelEnemyInLine, LevelInline, ]
    list_filter = ("difficulty", "enemy_leader_id")
    list_display = ("id", "name", "starting_enemies_number", "difficulty",
                    "number_of_enemies", "enemy_leader", "get_related_levels", "x", "y")
    list_display_links = ("id", "name", "starting_enemies_number",
                          "difficulty", "number_of_enemies",
                          "enemy_leader", "get_related_levels")


admin.site.register(Season)
