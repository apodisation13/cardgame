from rest_framework import serializers

from apps.enemies.models import Enemy, Level, LevelEnemy


class EnemySerializer(serializers.ModelSerializer):
    faction = serializers.CharField(source="faction.name")
    color = serializers.CharField(source="color.name")
    move = serializers.CharField(source="move.name")

    class Meta:
        model = Enemy
        fields = (
            "id",
            "name",
            "faction",
            "color",
            "move",
            "damage",
            "hp",
            "image",
            "shield",
        )


class LevelEnemySerializer(serializers.ModelSerializer):

    class Meta:
        model = LevelEnemy
        fields = ("enemy", )


class LevelSerializer(serializers.ModelSerializer):
    # l = LevelEnemySerializer(many=True, read_only=True)
    enemies = EnemySerializer(many=True, read_only=True)

    class Meta:
        model = Level
        fields = (
            "id",
            "name",
            "starting_enemies_number",
            "difficulty",
            # "l",
            "enemies"
        )
