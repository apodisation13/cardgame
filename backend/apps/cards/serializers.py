from rest_framework import serializers

from apps.cards.models import Card, CardDeck, Deck, Faction, Leader


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

    class Meta:
        model = CardDeck
        fields = ("card", )


class FactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faction
        fields = ("name", )


class LeaderSerializer(serializers.ModelSerializer):
    faction = serializers.CharField(source="faction.name")
    ability = serializers.CharField(source="ability.name")

    class Meta:
        model = Leader
        fields = ("id", "name", "faction", "ability", "damage", "charges")


class DeckSerializer(serializers.ModelSerializer):
    d = CardDeckSerializer(many=True, )
    cards = CardSerializer(many=True, required=False)
    leader = LeaderSerializer(many=False, required=False)
    leader_id = serializers.PrimaryKeyRelatedField(source="leader", queryset=Leader.objects.all())

    class Meta:
        model = Deck
        fields = ("id", "name", "health", "d", "cards", "leader", "leader_id")

    def create(self, validated_data):
        print(validated_data)

        cards = validated_data.pop("d", None)  # если вопросы не пришли, то можно создать опрос
        print(cards)

        # leader = validated_data.pop("leader", None)
        # print(leader)
        # validated_data["leader"] = leader["id"]

        deck = super().create(validated_data)

        if cards:
            for position in cards:
                CardDeck.objects.create(deck=deck, **position)

        return deck
