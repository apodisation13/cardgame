from apps.cards.models import Leader, UserLeader, Card, UserCard


def get_user_cards(self, user_id, card_serializer):
    """
    Принимает на вход self из сериализатора, user_id и сериализатор карт.
    Возвращает все карты!
    Если у юзера нет такой карты - у неё count=0.
    """
    all_cards = Card.objects.select_related("faction", "color", "type",
                                            "ability", "passive_ability").all()
    user_cards = UserCard.objects.filter(user_id=user_id).values("count",
                                                                 "card__pk",
                                                                 "pk").all()
    cards = []
    for card in all_cards:
        for user_card in user_cards:
            if card.pk == user_card["card__pk"]:
                cards.append({
                    "card": card_serializer(card, context={
                        "request": self.context["request"]}).data,
                    "count": user_card["count"],
                    "id": user_card["pk"],
                    # передаем id записи UserCard, с фронта по ней patch делается
                })
                break
        else:
            cards.append({
                "card": card_serializer(card, context={
                    "request": self.context["request"]}).data,
                "count": 0,
            })
    print(len(cards), "КАРТЫ")
    return cards


def get_user_leaders(self, user_id, leader_serializer):
    """
    Принимает на вход self из сериализатора, user_id и сериализатор лидеров.
    Возвращает все карты лидеров!
    Если у юзера нет такого лидера - у него count=0.
    """
    all_leaders = Leader.objects.select_related("faction", "ability",
                                                "passive_ability").all()
    user_leaders = UserLeader.objects.filter(user_id=user_id).values("count",
                                                                     "leader__pk",
                                                                     "pk").all()
    leaders = []
    for leader in all_leaders:
        for user_leader in user_leaders:
            if leader.pk == user_leader["leader__pk"]:
                leaders.append({
                    "card": leader_serializer(leader, context={
                        "request": self.context["request"]}).data,
                    "count": user_leader["count"],
                    "id": user_leader["pk"],
                    # передаем id записи UserLeader, с фронта по ней patch делается
                })
                break
        else:
            leaders.append({
                "card": leader_serializer(leader, context={
                    "request": self.context["request"]}).data,
                "count": 0,
            })
    print(len(leaders), "ЛИДЕРЫ")
    return leaders
