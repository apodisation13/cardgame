from rest_framework import serializers

from apps.accounts.models import CustomUser
from apps.cards.models import Card, Leader, UserCard, UserDeck, UserLeader
from apps.cards.serializers import CardSerializer, DeckSerializer, LeaderSerializer
from apps.enemies.models import Level
from apps.enemies.serializers import LevelSerializer, UserLevelsThroughSerializer


class UserCardsThroughSerializer(serializers.ModelSerializer):
    card = CardSerializer(many=False)  # если это не указать,то будет просто card_id, count

    class Meta:
        model = UserCard
        fields = ("card", "count", "id")


class UserLeadersThroughSerializer(serializers.ModelSerializer):
    card = LeaderSerializer(many=False, source='leader')

    class Meta:
        model = UserLeader
        fields = ("card", "count", "id")


class UserDecksThroughSerializer(serializers.ModelSerializer):
    """этот используется для user-database, где всё полностью"""
    deck = DeckSerializer(many=False)

    class Meta:
        model = UserDeck
        fields = ("id", "deck", "user")


class UserDatabaseSerializer(serializers.ModelSerializer):

    u_c = UserCardsThroughSerializer(many=True)
    locked_cards = serializers.SerializerMethodField()

    u_l = UserLeadersThroughSerializer(many=True)
    locked_leaders = serializers.SerializerMethodField()

    # decks = DeckSerializer(many=True)  # FIXME: а тут почему-то работает
    u_d = UserDecksThroughSerializer(many=True)

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
            "u_l",
            "locked_leaders",
            # "decks",
            "u_level",
            "locked_levels",
            "u_d",
        )

    def get_locked_cards(self, user):
        user_id = user.id
        user_locked_cards = Card.objects.\
            select_related("faction", "color", "type", "ability", "passive_ability").\
            exclude(u_c__user_id=user_id).\
            all()
        c = []
        for u in user_locked_cards:
            s = {'card': CardSerializer(u, context={'request': self.context.get('request')}).data, 'count': 0}
            c.append(s)
        return c

    def get_locked_leaders(self, user):
        user_id = user.id
        user_locked_leaders = Leader.objects.\
            select_related("faction", "ability", "passive_ability").\
            exclude(u_l__user_id=user_id).\
            all()
        c = []
        for u in user_locked_leaders:
            s = {'card': LeaderSerializer(u, context={'request': self.context.get('request')}).data, 'count': 0}
            c.append(s)
        return c

    def get_locked_levels(self, user):
        user_id = user.id
        user_locked_levels = Level.objects.\
            select_related("enemy_leader__ability", "enemy_leader__faction").\
            prefetch_related("enemies__faction", "enemies__color", "enemies__move", "enemies__passive_ability").\
            exclude(u_level__user_id=user_id).\
            all()
        c = []
        for u in user_locked_levels:
            s = {'level': LevelSerializer(u, context={'request': self.context.get('request')}).data}
            c.append(s)
        return c
