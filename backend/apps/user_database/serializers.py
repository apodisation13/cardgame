from rest_framework import serializers

from apps.accounts.models import CustomUser
from apps.cards.models import Card, Leader, UserCard, UserDeck, UserLeader
from apps.cards.serializers import CardSerializer, DeckSerializer, LeaderSerializer
from apps.enemies.models import Level, UserLevel
from apps.enemies.serializers import LevelSerializer


class UserCardsThroughSerializer(serializers.ModelSerializer):
    card = CardSerializer(many=False)  # если это не указать,то будет просто card_id, count

    class Meta:
        model = UserCard
        fields = ("card", "count", "id")


#
#
# class UserLeadersThroughSerializer(serializers.ModelSerializer):
#     card = LeaderSerializer(many=False, source='leader')
#
#     class Meta:
#         model = UserLeader
#         fields = ("card", "count", "id")


class UserDecksThroughSerializer(serializers.ModelSerializer):
    """этот используется для user-database, где всё полностью"""
    deck = DeckSerializer(many=False)

    class Meta:
        model = UserDeck
        fields = ("id", "deck", "user")


class UserDatabaseSerializer(serializers.ModelSerializer):
    # cards = serializers.SerializerMethodField()
    # leaders = serializers.SerializerMethodField()
    levels = serializers.SerializerMethodField()

    # u_d = UserDecksThroughSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            # "cards",
            # "leaders",
            "levels",
            # "u_d",
        )

    def get_cards(self, user):
        user_id = user.id
        all_cards = Card.objects.select_related("faction", "color", "type", "ability", "passive_ability").all()
        user_cards = UserCard.objects.filter(user_id=user_id).values("count", "card__pk", "pk").all()
        cards = []
        for card in all_cards:
            for user_card in user_cards:
                if card.pk == user_card["card__pk"]:
                    cards.append({
                        "card": CardSerializer(card, context={"request": self.context["request"]}).data,
                        "count": user_card["count"],
                        "id": user_card["pk"],  # передаем id записи UserCard, с фронта по ней patch делается
                    })
                    break
            else:
                cards.append({
                    "card": CardSerializer(card, context={"request": self.context["request"]}).data,
                    "count": 0,
                })
        print(len(cards), "КАРТЫ")
        return cards

    def get_leaders(self, user):
        user_id = user.id
        all_leaders = Leader.objects.select_related("faction", "ability", "passive_ability").all()
        user_leaders = UserLeader.objects.filter(user_id=user_id).values("count", "leader__pk", "pk").all()
        leaders = []
        for leader in all_leaders:
            for user_leader in user_leaders:
                if leader.pk == user_leader["leader__pk"]:
                    leaders.append({
                        "card": LeaderSerializer(leader, context={"request": self.context["request"]}).data,
                        "count": user_leader["count"],
                        "id": user_leader["pk"],  # передаем id записи UserLeader, с фронта по ней patch делается
                    })
                    break
            else:
                leaders.append({
                    "card": LeaderSerializer(leader, context={"request": self.context["request"]}).data,
                    "count": 0,
                })
        print(len(leaders), "ЛИДЕРЫ")
        return leaders

    def get_levels(self, user):
        user_id = user.id
        all_levels = Level.objects. \
            select_related("enemy_leader__ability", "enemy_leader__faction"). \
            prefetch_related(
                "enemies__faction",
                "enemies__color",
                "enemies__move",
                "enemies__passive_ability",
                "related_levels",
            ). \
            all()
        user_levels = UserLevel.objects.filter(user_id=user_id).values("level__pk", "pk", "finished").all()
        levels = []
        for level in all_levels:
            for user_level in user_levels:
                if level.pk == user_level["level__pk"]:
                    levels.append({
                        "level": LevelSerializer(level, context={"request": self.context.get("request")}).data,
                        # передаем id записи UserLevel, по ней делается запрос на открытие связанных уровней
                        "id": user_level["pk"],
                        "unlocked": True,  # уровень считается открытым, если есть запись в связанной таблице UserLevel
                        "finished": user_level["finished"],  # открытый уровень может быть пройден, а может нет
                    })
                    break
            # если уровень не нашелся в открытых, значит идем сюда и добавляем его с флажком закрыт (False)
            else:
                levels.append({
                    "level": LevelSerializer(level, context={"request": self.context.get("request")}).data,
                    "unlocked": False,
                })
        print(len(levels), "УРОВНИ")
        return levels


class UserResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("scraps", "wood", "kegs", "big_kegs", "chests")
