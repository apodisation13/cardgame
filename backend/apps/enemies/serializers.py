from rest_framework import serializers

from apps.core.serializers import EnemyLeaderAbilitySerializer, EnemyPassiveAbilitySerializer, MoveSerializer
from apps.enemies.models import Enemy, EnemyLeader, Level


class EnemySerializer(serializers.ModelSerializer):
    faction = serializers.CharField(source="faction.name")
    color = serializers.CharField(source="color.name")
    move = MoveSerializer(many=False, read_only=True)
    passive_ability = EnemyPassiveAbilitySerializer(many=False, read_only=True)

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
            "passive",
            "passive_ability",
            "passive_increase_damage",
            "passive_heal",
            "passive_heal_leader",
            "passive_damage",
        )


class EnemyLeaderSerializer(serializers.ModelSerializer):
    faction = serializers.CharField(source="faction.name")
    ability = EnemyLeaderAbilitySerializer(many=False, read_only=True)

    class Meta:
        model = EnemyLeader
        fields = (
            "id",
            "name",
            "faction",
            "image",
            "passive",
            "hp",
            "ability",
            "damage_once",
            "damage_per_turn",
            "heal_self_per_turn",
        )


class LevelSerializer(serializers.ModelSerializer):
    enemies = EnemySerializer(many=True, read_only=True)
    enemy_leader = EnemyLeaderSerializer(many=False, read_only=True)

    class Meta:
        model = Level
        fields = (
            "id",
            "name",
            "starting_enemies_number",
            "difficulty",
            "enemies",
            "enemy_leader",
        )
