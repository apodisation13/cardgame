from django.contrib import admin

from apps.cards.models import Ability, Card, CardDeck, Color, Deck, Faction, Type, Leader

admin.site.register(Faction)
admin.site.register(Color)
admin.site.register(Type)
admin.site.register(Ability)
admin.site.register(Card)
admin.site.register(Leader)


class CardDeckInLine(admin.TabularInline):
    model = CardDeck


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    inlines = [CardDeckInLine, ]
