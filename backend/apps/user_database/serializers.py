from rest_framework import serializers

from apps.accounts.models import CustomUser
from apps.cards.models import Card, Leader, UserCard, UserDeck, UserLeader
from apps.cards.serializers import CardSerializer, DeckSerializer, LeaderSerializer
from apps.enemies.models import Level, UserLevel
from apps.enemies.serializers import LevelSerializer

# class UserCardsThroughSerializer(serializers.ModelSerializer):
#     card = CardSerializer(many=False)  # если это не указать,то будет просто card_id, count
#
#     class Meta:
#         model = UserCard
#         fields = ("card", "count", "id")
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

    # u_c = UserCardsThroughSerializer(many=True)
    # locked_cards = serializers.SerializerMethodField()
    #
    # u_l = UserLeadersThroughSerializer(many=True)
    # locked_leaders = serializers.SerializerMethodField()

    # decks = DeckSerializer(many=True)  # FIXME: а тут почему-то работает

    cards = serializers.SerializerMethodField()
    leaders = serializers.SerializerMethodField()
    levels = serializers.SerializerMethodField()

    u_d = UserDecksThroughSerializer(many=True)
    #
    # u_level = UserLevelsThroughSerializer(many=True)
    # locked_levels = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "cards",
            "leaders",
            "levels",
            # "u_c",
            # "locked_cards",
            # "u_l",
            # "locked_leaders",
            # "decks",
            # "u_level",
            # "locked_levels",
            "u_d",
        )

    def get_cards(self, user):
        user_id = user.id
        all_cards = Card.objects.select_related("faction", "color", "type", "ability", "passive_ability").all()
        cards = []
        for card in all_cards:
            usercard = UserCard.objects.filter(card=card, user_id=user_id).first()
            if usercard:
                cards.append({
                    "card": CardSerializer(card, context={"request": self.context["request"]}).data,
                    "count": usercard.count,
                    "id": usercard.id,
                })
            else:
                cards.append({
                    "card": CardSerializer(card, context={"request": self.context["request"]}).data,
                    "count": 0,
                })
        return cards

    def get_leaders(self, user):
        user_id = user.id
        all_leaders = Leader.objects.select_related("faction", "ability", "passive_ability").all()
        leaders = []
        for leader in all_leaders:
            userleader = UserLeader.objects.filter(leader=leader, user_id=user_id).first()
            if userleader:
                leaders.append({
                    "card": LeaderSerializer(leader, context={"request": self.context["request"]}).data,
                    "count": userleader.count,
                    "id": userleader.id,
                })
            else:
                leaders.append({
                    "card": LeaderSerializer(leader, context={"request": self.context["request"]}).data,
                    "count": 0,
                })
        return leaders

    def get_levels(self, user):
        user_id = user.id
        all_levels = Level.objects.\
            select_related("enemy_leader__ability", "enemy_leader__faction").\
            prefetch_related("enemies__faction", "enemies__color", "enemies__move", "enemies__passive_ability").\
            all()
        levels = []
        for level in all_levels:
            userlevel = UserLevel.objects.filter(level=level, user_id=user_id).first()
            if userlevel:
                levels.append({
                    'level': LevelSerializer(level, context={'request': self.context.get('request')}).data,
                    'id': userlevel.id,
                })
            else:
                levels.append({
                    'level': LevelSerializer(level, context={'request': self.context.get('request')}).data,
                })
        return levels


class UserResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("scraps", "wood", "kegs", "big_kegs", "chests")
