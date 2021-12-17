from django.contrib import admin

from apps.cards.models import Faction, Color, Type, Ability, Card

admin.site.register(Faction)
admin.site.register(Color)
admin.site.register(Type)
admin.site.register(Ability)
admin.site.register(Card)
