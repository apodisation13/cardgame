from django.contrib import admin

from apps.core.models import (
    Ability,
    Color,
    Deathwish,
    EnemyLeaderAbility,
    EnemyPassiveAbility,
    Faction,
    GameConst,
    Move,
    PassiveAbility,
    Type,
)


@admin.register(GameConst)
class UserActionsJsonAdmin(admin.ModelAdmin):
    model = GameConst

    """Запрет на добавление"""
    def has_add_permission(self, request, obj=None):
        first_data = GameConst.objects.first()
        return not first_data

    """Запрет на удаление"""
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Faction)
admin.site.register(Color)
admin.site.register(Type)
admin.site.register(Ability)
admin.site.register(PassiveAbility)
admin.site.register(Move)
admin.site.register(EnemyLeaderAbility)
admin.site.register(EnemyPassiveAbility)
admin.site.register(Deathwish)
