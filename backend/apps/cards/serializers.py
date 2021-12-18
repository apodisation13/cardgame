from rest_framework import serializers

from apps.cards.models import Card, Try, CardDeck, Deck


class CardSerializer(serializers.ModelSerializer):
    faction = serializers.CharField(source="faction.name")
    color = serializers.CharField(source="color.name")
    type = serializers.CharField(source="type.name")
    ability = serializers.CharField(source="ability.name")

    class Meta:
        model = Card
        fields = (
            "id",
            "faction",
            "color",
            "type",
            "ability",
            "charges",
            "damage",
            "hp",
            "heal"
        )


class TrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Try
        fields = ("id", "name")


class CardDeckSerializer(serializers.ModelSerializer):
    card = CardSerializer(many=False, read_only=True)

    class Meta:
        model = CardDeck
        fields = ("card", )


class DeckSerializer(serializers.ModelSerializer):
    d = CardDeckSerializer(many=True, )

    class Meta:
        model = Deck
        fields = ("id", "name", "health", "d")
        # depth = 1

    def create(self, validated_data):
        print(validated_data)
        cards = validated_data.pop('d', None)  # если вопросы не пришли, то можно создать опрос
        print(cards)

        deck = super().create(validated_data)

        if cards:
            for position in cards:
                CardDeck.objects.create(deck=deck, **position)

        return deck
