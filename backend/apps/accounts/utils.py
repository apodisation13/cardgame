# from apps.cards.models import Card, UserCard
from django.apps import apps


def set_unlocked_cards(user):
    """
    эта функция выполняется 1 раз, когда регистрируется новый юзер.
    при этом ему добавляются все открытые карты, лидеры, уровни, по одной через поле count=1
    добавление через UserCard, UserLeader, UserLevel
    """

    # чтобы избежать ошибки цикличности импорта!
    Card = apps.get_model('cards.Card')
    UserCard = apps.get_model('cards.UserCard')

    # Сохранение карт юзеру
    unlocked_cards = Card.objects.filter(unlocked=True).all()

    for card in unlocked_cards:
        UserCard.objects.create(card_id=card.id, user_id=user.id)
        print(f'Для юзера {user.id}, {user.username} открыли карту {card.id}')

    # просто проверка что все карты загрузились
    cards = UserCard.objects.filter(user_id=user.id).all()
    print(len(cards))  # вот здесь должно быть столько, сколько в базе открытых карт

    # чтобы избежать ошибки цикличности импорта!
    Leader = apps.get_model('cards.Leader')
    UserLeader = apps.get_model('cards.UserLeader')

    # Сохранение лидеров юзеру
    unlocked_leaders = Leader.objects.filter(unlocked=True).all()
    for leader in unlocked_leaders:
        UserLeader.objects.create(leader_id=leader.id, user_id=user.id)
        print(f'Для юзера {user.id}, {user.username} открыли лидера {leader.id}')

    # просто проверка что все лидеры загрузились
    leaders = UserLeader.objects.filter(user_id=user.id).all()
    print(len(leaders))  # вот здесь должно быть столько, сколько в базе открытых лидеров

    # Сохранение колоды base-deck (id=1), в которой есть все открытые карты и открытый лидер
    UserDeck = apps.get_model('cards.UserDeck')
    UserDeck.objects.create(deck_id=1, user_id=user.id)

    # Сохранение уровней
    Level = apps.get_model('enemies.Level')
    UserLevel = apps.get_model('enemies.UserLevel')

    unlocked_levels = Level.objects.filter(unlocked=True).all()
    for level in unlocked_levels:
        UserLevel.objects.create(level_id=level.id, user_id=user.id)
        print(f'Для юзера {user.id}, {user.username} открыли уровень {level.id}')

    # просто проверка что все уровни загрузились
    levels = UserLevel.objects.filter(user_id=user.id).all()
    print(len(levels))  # вот здесь должно быть столько, сколько в базе открытых лидеров
