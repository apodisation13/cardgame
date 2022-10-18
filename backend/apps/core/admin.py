from apps.core.models import (Ability, Color, EnemyLeaderAbility,
                              EnemyPassiveAbility, Faction, Move,
                              PassiveAbility, Type, UserActionsJson)
from django.contrib import admin


@admin.register(UserActionsJson)
class UserActionsJsonAdmin(admin.ModelAdmin):
    model = UserActionsJson
    """Запрет на добавление"""
    def has_add_permission(self, request, obj=None):
        user_j = UserActionsJson.objects.first()
        if user_j:
            return False
        return True

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
