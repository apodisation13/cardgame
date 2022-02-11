from django.contrib import admin

from apps.enemies.models import Enemy, Level, LevelEnemy, Move

admin.site.register(Move)
admin.site.register(Enemy)


class LevelEnemyInLine(admin.TabularInline):
    model = LevelEnemy


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    inlines = [LevelEnemyInLine, ]
