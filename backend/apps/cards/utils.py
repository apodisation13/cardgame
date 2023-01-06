from django.apps import apps
from django.db.models import Count, F, Sum

from apps.core.models import GameConst


def change_decks_health(card_id, diff):
    """Изменяет health у ВСЕХ колод, содержащих card_id, на diff (при изменении жизни какой-либо карты в админке)"""
    Deck = apps.get_model('cards.Deck')
    decks = Deck.objects.filter(d__card_id=card_id).prefetch_related('d__deck')
    for deck in decks:
        deck.health = F('health') + diff
        deck.save()
    print(f"Deck health changed for {len(decks)} decks")


def get_cards_to_mill(user_cards):
    """Возвращает для юзера список словарей вида
    {color: цвет карт,
     mill_count: количество карт этого цвета, которое можно уничтожить, оставив по одной,
     scraps_for_card: количество ресурсов, возвращаемых при уничтожении одной карты этого цвета
    }
    """
    cards_to_mill = user_cards.values(
        color=F('card__color__name')
    ).annotate(
        mill_count=Sum('count') - Count('card'),
    )
    game_const = GameConst.objects.first().data
    for item in cards_to_mill:
        item['scraps_for_card'] = game_const[f"mill_{item['color'].lower()}"]

    return cards_to_mill
