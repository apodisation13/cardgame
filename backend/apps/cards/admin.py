from django.contrib import admin

from apps.cards.models import Faction, Color, Type, Ability, Card, Try, CardDeck, Deck

admin.site.register(Faction)
admin.site.register(Color)
admin.site.register(Type)
admin.site.register(Ability)
admin.site.register(Card)
admin.site.register(Try)


class CardDeckInLine(admin.TabularInline):
    model = CardDeck


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    inlines = [CardDeckInLine, ]
