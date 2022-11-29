from django.apps import apps
from django.db.models import F


def change_decks_health(card_id, diff):
    """Изменяет health у ВСЕХ колод, содержащих card_id, на diff (при изменении жизни какой-либо карты в админке)"""
    Deck = apps.get_model('cards.Deck')
    decks = Deck.objects.filter(d__card_id=card_id).prefetch_related('d__deck')
    for deck in decks:
        deck.health = F('health') + diff
        deck.save()
    print(f"Deck health changed for {len(decks)} decks")
