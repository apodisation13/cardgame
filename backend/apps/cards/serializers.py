from rest_framework import serializers

from apps.cards.models import Card, CardDeck, Deck


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


class CardDeckSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(source="card.id")
    # faction = serializers.CharField(source="card.faction.name")
    # color = serializers.CharField(source="card.color.name")
    # type = serializers.CharField(source="card.type.name")
    # ability = serializers.CharField(source="card.ability.name")
    # charges = serializers.IntegerField(source="card.charges")
    # damage = serializers.IntegerField(source="card.damage")
    # hp = serializers.IntegerField(source="card.hp")
    # heal = serializers.IntegerField(source="card.heal")
    # card = CardSerializer(many=False, )

    class Meta:
        model = CardDeck
        # fields = (
        #     "id",
        #     "faction",
        #     "color",
        #     "type",
        #     "ability",
        #     "charges",
        #     "damage",
        #     "hp",
        #     "heal",
        # )
        fields = ("card", )


class DeckSerializer(serializers.ModelSerializer):
    d = CardDeckSerializer(many=True, )
    cards = CardSerializer(many=True, required=False)

    class Meta:
        model = Deck
        fields = ("id", "name", "health", "d", "cards")


    def create(self, validated_data):
        print(validated_data)
        cards = validated_data.pop('d', None)  # если вопросы не пришли, то можно создать опрос
        print(cards)

        deck = super().create(validated_data)

        if cards:
            for position in cards:
                CardDeck.objects.create(deck=deck, **position)

        return deck
