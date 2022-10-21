from apps.accounts.models import CustomUser
from apps.cards.models import Card, Leader, UserCard, UserDeck, UserLeader
from apps.cards.serializers import (CardSerializer, DeckSerializer,
                                    LeaderSerializer)
from apps.enemies.serializers import (EnemyLeaderSerializer, EnemySerializer,
                                      LevelSerializer)
from apps.enemies.utils import get_opened_user_levels
from rest_framework import serializers


class UserDecksThroughSerializer(serializers.ModelSerializer):
    """этот используется для user-database, где всё полностью"""
    deck = DeckSerializer(many=False)

    class Meta:
        model = UserDeck
        fields = ("id", "deck", "user")


class UserDatabaseSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    leaders = serializers.SerializerMethodField()
    levels = serializers.SerializerMethodField()

    u_d = UserDecksThroughSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "cards",
            "leaders",
            "levels",
            "u_d",
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
        levels = get_opened_user_levels(self=self, user_id=user.id, level_serializer=LevelSerializer)
        return levels


class UserResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("scraps", "wood", "kegs", "big_kegs", "chests")


class DatabaseSerializer(serializers.Serializer):
    user_database = UserDatabaseSerializer()
    resources = UserResourceSerializer()
    enemies = EnemySerializer(many=True)
    enemy_leaders = EnemyLeaderSerializer(many=True)
