from django.contrib import admin

from apps.enemies.models import Enemy, EnemyLeader, Level, LevelEnemy, LevelRelatedLevels, Season


@admin.register(EnemyLeader)
class EnemyLeaderAdmin(admin.ModelAdmin):
    model = EnemyLeader
    list_filter = ("faction_id", "ability_id", "has_passive", "passive_ability_id")
    list_display = [field.name for field in EnemyLeader._meta.fields]
    list_display_links = [field.name for field in EnemyLeader._meta.fields]


@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    model = Enemy
    list_filter = ("faction_id", "color_id", "move_id", "has_passive", "passive_ability_id",
                   "has_deathwish", "deathwish")
    list_display = [field.name for field in Enemy._meta.fields]
    list_display_links = [field.name for field in Enemy._meta.fields]
    search_fields = ['name']


class LevelEnemyInLine(admin.TabularInline):
    model = LevelEnemy
    extra = 0
    verbose_name_plural = 'level enemies'
    autocomplete_fields = ['enemy']


class LevelInline(admin.TabularInline):
    model = LevelRelatedLevels
    fk_name = "level"
    fields = ("line", "related_level")
    extra = 0
    verbose_name_plural = 'level related levels'
    autocomplete_fields = ['related_level']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    inlines = [LevelEnemyInLine, LevelInline, ]
    list_filter = ("difficulty", "enemy_leader_id", "season")
    list_display = ("id", "name", "starting_enemies_number_admin", "difficulty", "enemy_leader_admin",
                    "number_of_enemies_admin", "get_related_levels", "x", "y", "season")
    list_display_links = ("id", "name", "starting_enemies_number_admin", "enemy_leader_admin",
                          "difficulty", "number_of_enemies_admin",
                          "get_related_levels", "season")
    search_fields = ['name']

    @admin.display(description="enemy_leader")
    def enemy_leader_admin(self, obj):
        return f"{obj.enemy_leader.name} - {obj.enemy_leader.ability}"

    @admin.display(description="st_en_№")
    def starting_enemies_number_admin(self, obj):
        return obj.starting_enemies_number

    @admin.display(description="en_№")
    def number_of_enemies_admin(self, obj):
        return obj.number_of_enemies()


admin.site.register(Season)
