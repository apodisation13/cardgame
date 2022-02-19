from django.contrib import admin

from apps.enemies.models import Enemy, EnemyLeader, EnemyLeaderAbility, Level, LevelEnemy, Move

admin.site.register(Move)
admin.site.register(Enemy)
admin.site.register(EnemyLeaderAbility)
admin.site.register(EnemyLeader)


class LevelEnemyInLine(admin.TabularInline):
    model = LevelEnemy


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    inlines = [LevelEnemyInLine, ]
