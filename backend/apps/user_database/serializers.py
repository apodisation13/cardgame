from rest_framework import serializers

from apps.accounts.models import CustomUser
from apps.cards.models import Card, Leader, UserCard, UserDeck, UserLeader
from apps.cards.serializers import CardSerializer, DeckSerializer, LeaderSerializer
from apps.core.serializers import GameConstSerializer
from apps.enemies.serializers import EnemyLeaderSerializer, EnemySerializer, SeasonSerializer

from .utils import get_user_cards, get_user_leaders


class UserDecksThroughSerializer(serializers.ModelSerializer):
    """этот используется для user-database, где всё полностью"""
    deck = DeckSerializer(many=False)

    class Meta:
        model = UserDeck
        fields = ("id", "deck", "user")


class UserDatabaseSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    leaders = serializers.SerializerMethodField()
    # levels = serializers.SerializerMethodField()

    u_d = UserDecksThroughSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "cards",
            "leaders",
            # "levels",
            "u_d",
        )

    def get_cards(self, user):
        return get_user_cards(self=self, user_id=user.id, card_serializer=CardSerializer)

    def get_leaders(self, user):
        return get_user_leaders(self=self, user_id=user.id, leader_serializer=LeaderSerializer)

    # def get_levels(self, user):
    #     levels = get_opened_user_levels(self=self, user_id=user.id, level_serializer=LevelSerializer)
    #     return levels


class UserResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("scraps", "wood", "kegs", "big_kegs", "chests", "keys")


class DatabaseSerializer(serializers.Serializer):
    user_database = UserDatabaseSerializer(many=False)
    seasons = SeasonSerializer(many=True)
    resources = UserResourceSerializer(many=False)
    enemies = EnemySerializer(many=True)
    enemy_leaders = EnemyLeaderSerializer(many=True)
    game_const = GameConstSerializer(many=False)
