from rest_framework import serializers

from apps.accounts.models import CustomUser
from apps.cards.models import Card, Leader
from apps.cards.serializers import (  # UserDecksThroughSerializer,
    CardSerializer,
    DeckSerializer,
    LeaderSerializer,
    UserCardsThroughSerializer,
    UserLeadersThroughSerializer,
)
from apps.enemies.models import Level
from apps.enemies.serializers import UserLevelsThroughSerializer, LevelSerializer


class UserDatabaseSerializer(serializers.ModelSerializer):

    u_c = UserCardsThroughSerializer(many=True)
    # cards = CardSerializer(many=True)
    locked_cards = serializers.SerializerMethodField()

    # leaders = LeaderSerializer(many=True)
    u_l = UserLeadersThroughSerializer(many=True)
    locked_leaders = serializers.SerializerMethodField()

    decks = DeckSerializer(many=True)  # FIXME: а тут почему-то работает
    # u_d = UserDecksThroughSerializer(many=True)

    u_level = UserLevelsThroughSerializer(many=True)
    locked_levels = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "u_c",
            "locked_cards",
            # "cards",
            "u_l",
            "locked_leaders",
            # "leaders",
            "decks",
            # "u_d",
            "u_level",
            "locked_levels",
        )

    def get_locked_cards(self, user):
        user_id = user.id
        user_locked_cards = Card.objects.exclude(u_c__user_id=user_id).all()
        return CardSerializer(user_locked_cards, many=True).data

    def get_locked_leaders(self, user):
        user_id = user.id
        user_locked_leaders = Leader.objects.exclude(u_l__user_id=user_id).all()
        return LeaderSerializer(user_locked_leaders, many=True).data

    def get_locked_levels(self, user):
        user_id = user.id
        user_locked_levels = Level.objects.exclude(u_level__user_id=user_id).all()
        return LevelSerializer(user_locked_levels, many=True).data
