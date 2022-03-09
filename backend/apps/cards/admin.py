from django.contrib import admin

from apps.cards.models import Ability, Card, CardDeck, Deck, Leader, Type

admin.site.register(Type)
admin.site.register(Ability)


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    model = Leader
    list_filter = ("faction_id", "ability_id", "passive")  # по каким полям фильтр, выбор
    list_display = [field.name for field in Leader._meta.fields]  # показать все поля таблицы
    list_display_links = [field.name for field in Leader._meta.fields]  # кликабельны так же все поля


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    model = Card
    list_filter = ("faction_id", "color_id", "type_id", "ability_id")
    list_display = [field.name for field in Card._meta.fields]
    list_display_links = [field.name for field in Card._meta.fields]


class CardDeckInLine(admin.TabularInline):
    model = CardDeck


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    inlines = [CardDeckInLine, ]
    list_filter = ("leader_id", )
    list_display = [field.name for field in Deck._meta.fields]
    list_display_links = [field.name for field in Deck._meta.fields]
