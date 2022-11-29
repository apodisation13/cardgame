from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.accounts.models import CustomUser
from apps.cards.models import UserDeck
from apps.cards.serializers import CardSerializer, DeckSerializer, LeaderSerializer
from apps.core.serializers import GameConstSerializer
from apps.enemies.serializers import EnemyLeaderSerializer, EnemySerializer, SeasonSerializer
from apps.user_database.utils import get_cards_for_user, get_leaders_for_user


class UserDecksThroughSerializer(serializers.ModelSerializer):
    """этот используется для user-database, где всё полностью"""
    deck = DeckSerializer(many=False)

    class Meta:
        model = UserDeck
        fields = ("id", "deck", "user")


class UserDatabaseSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    leaders = serializers.SerializerMethodField()

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

    @extend_schema_field(CardSerializer(many=True))
    def get_cards(self, user):
        return get_cards_for_user(self=self, user_id=user.id, card_serializer=CardSerializer)

    @extend_schema_field(LeaderSerializer(many=True))
    def get_leaders(self, user):
        return get_leaders_for_user(self=self, user_id=user.id, leader_serializer=LeaderSerializer)


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
