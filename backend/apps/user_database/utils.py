from apps.cards.models import Card, Leader, UserCard, UserLeader
from apps.enemies.models import Level, UserLevel


def get_opened_user_levels(self, user_id, level_serializer, season_id):
    """
    Принимает на вход self из сериализатора, user_id, сериализатор уровней (иначе circular import)
    Возвращает все уровни юзера по сезону!
    Если мы приходим из вызова всей базы данных, то сюда заходим с каждым сезоном
    """
    all_levels = Level.objects.\
        select_related("enemy_leader__ability", "enemy_leader__faction", "season").\
        prefetch_related(
            "enemies__faction",
            "enemies__color",
            "enemies__move",
            "enemies__passive_ability",
            "enemies__deathwish",
            "related_levels",
            "children",
        ).filter(season_id=season_id).\
        all()
    user_levels = UserLevel.objects.filter(user_id=user_id).values("level__pk", "pk", "finished").all()
    levels = []
    for level in all_levels:
        for user_level in user_levels:
            if level.pk == user_level["level__pk"]:
                levels.append({
                    "level": level_serializer(level, context={"request": self.context.get("request")}).data,
                    "id": user_level["pk"],  # id записи UserLevel, пойдет при прохождении как finished_level
                    "unlocked": True,  # уровень считается открытым, если есть запись в связанной таблице UserLevel
                    "finished": user_level["finished"],  # открытый уровень может быть пройден, а может нет
                })
                break
        # если уровень не нашелся в открытых, значит идем сюда и добавляем его с флажком закрыт (False)
        else:
            levels.append({
                "level": level_serializer(level, context={"request": self.context.get("request")}).data,
                "unlocked": False,
            })
    print(len(levels), "УРОВНИ")
    return levels


def get_cards_for_user(self, user_id, card_serializer):
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


def get_leaders_for_user(self, user_id, leader_serializer):
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
