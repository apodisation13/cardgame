from rest_framework import serializers

from apps.cards.models import Card, CardDeck, Deck, Leader, UserCard, UserDeck, UserLeader
from apps.core.serializers import AbilitySerializer, PassiveAbilitySerializer


class CardSerializer(serializers.ModelSerializer):
    faction = serializers.CharField(source="faction.name")
    color = serializers.CharField(source="color.name")
    type = serializers.CharField(source="type.name")
    ability = AbilitySerializer(many=False, read_only=True)
    passive_ability = PassiveAbilitySerializer(many=False, read_only=True)

    class Meta:
        model = Card
        fields = (
            "id",
            "name",
            "unlocked",
            "faction",
            "color",
            "type",
            "ability",
            "charges",
            "damage",
            "hp",
            "heal",
            "image",
            "has_passive",
            "has_passive_in_hand",
            "passive_ability",
        )


class CardDeckSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardDeck
        fields = ("card", )


class LeaderSerializer(serializers.ModelSerializer):
    faction = serializers.CharField(source="faction.name")
    ability = AbilitySerializer(many=False, read_only=True)
    passive_ability = PassiveAbilitySerializer(many=False, read_only=True)

    class Meta:
        model = Leader
        fields = (
            "id",
            "name",
            "unlocked",
            "faction",
            "ability",
            "damage",
            "charges",
            "image",
            "has_passive",
            "passive_ability"
        )


class DeckSerializer(serializers.ModelSerializer):
    d = CardDeckSerializer(many=True, )
    cards = CardSerializer(many=True, required=False)
    leader = LeaderSerializer(many=False, required=False)
    leader_id = serializers.PrimaryKeyRelatedField(source="leader",
                                                   queryset=Leader.objects.select_related("faction", "ability", "passive_ability").all())

    class Meta:
        model = Deck
        fields = ("id", "name", "health", "d", "cards", "leader", "leader_id")

    def create(self, validated_data):
        print(validated_data)

        cards = validated_data.pop("d", None)
        print(cards)

        deck = super().create(validated_data)

        if cards:
            for position in cards:
                CardDeck.objects.create(deck=deck, **position)

        return deck

    def update(self, instance, validated_data):
        """изменение колоды - карт или лидера"""
        cards = validated_data.pop("d", None)
        print(cards)

        deck = super().update(instance, validated_data)

        # ищем записи по id колоды, обновляем все карты внутри них
        # FIXME: будет глюк если в колоде будет не ровно 12 карт, а допустим не менее 20. было 22, пришло 20, ГЛЮК
        current_cards = CardDeck.objects.filter(deck_id=deck.id)
        for i in range(len(current_cards)):
            print(current_cards[i].id, cards[i].get('card').id)
            carddeck = CardDeck.objects.filter(id=current_cards[i].id).first()
            carddeck.card_id = cards[i].get('card').id
            carddeck.save()

        return deck


class UserCardsThroughSerializer(serializers.ModelSerializer):
    card = CardSerializer(many=False)  # если это не указать,то будет просто card_id, count

    class Meta:
        model = UserCard
        fields = ("card", "count", "id")


class UserLeadersThroughSerializer(serializers.ModelSerializer):
    leader = LeaderSerializer(many=False)

    class Meta:
        model = UserLeader
        fields = ("leader", "count", "id")


class CraftUserCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCard
        fields = ("id", "user", "card", "count")

    def update(self, instance, validated_data):
        validated_data['count'] += 1  # ВОТ ЭТО САМОЕ ГЛАВНОЕ! Увеличиваем на 1 запас ЭТОЙ КАРТЫ у юзера
        return super().update(instance, validated_data)


class MillUserCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCard
        fields = ("id", "user", "card", "count")

    def update(self, instance, validated_data):
        validated_data['count'] -= 1

        if validated_data['count'] != 0:
            return super().update(instance, validated_data)

        instance.delete()
        return instance


class CraftUserLeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLeader
        fields = ("id", "user", "leader", "count")

    def update(self, instance, validated_data):
        validated_data['count'] += 1  # ВОТ ЭТО САМОЕ ГЛАВНОЕ! Увеличиваем на 1 запас ЭТОЙ КАРТЫ у юзера
        return super().update(instance, validated_data)


class MillUserLeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLeader
        fields = ("id", "user", "leader", "count")

    def update(self, instance, validated_data):
        validated_data['count'] -= 1

        if validated_data['count'] != 0:
            return super().update(instance, validated_data)

        instance.delete()
        return instance


class UserDecksThroughSerializer(serializers.ModelSerializer):
    deck = DeckSerializer(many=False)

    class Meta:
        model = UserDeck
        fields = ("id", "deck", "user")
