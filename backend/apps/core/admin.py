from django.contrib import admin

from apps.core.models import (
    Ability,
    Color,
    EnemyLeaderAbility,
    EnemyPassiveAbility,
    Faction,
    Move,
    PassiveAbility,
    Type,
)

admin.site.register(Faction)
admin.site.register(Color)
admin.site.register(Type)
admin.site.register(Ability)
admin.site.register(PassiveAbility)
admin.site.register(Move)
admin.site.register(EnemyLeaderAbility)
admin.site.register(EnemyPassiveAbility)
