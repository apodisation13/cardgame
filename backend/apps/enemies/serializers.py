from rest_framework import serializers

from apps.core.serializers import EnemyLeaderAbilitySerializer, EnemyPassiveAbilitySerializer, MoveSerializer
from apps.enemies.models import Enemy, EnemyLeader, Level, LevelRelatedLevels, UserLevel
from apps.enemies.utils import get_opened_user_levels


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
            "has_passive",
            "passive_ability",
            "passive_increase_damage",
            "passive_heal",
            "passive_heal_leader",
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
            "has_passive",
            "hp",
            "ability",
            "damage_once",
            "damage_per_turn",
            "heal_self_per_turn",
        )


class RelatedLevelThroughSerializer(serializers.ModelSerializer):

    class Meta:
        model = LevelRelatedLevels
        fields = ("line", "connection", "related_level_id")


class LevelSerializer(serializers.ModelSerializer):
    enemies = EnemySerializer(many=True, read_only=True)
    enemy_leader = EnemyLeaderSerializer(many=False, read_only=True)
    children = RelatedLevelThroughSerializer(many=True)

    class Meta:
        model = Level
        fields = (
            "id",
            "name",
            "children",
            "related_levels",
            "x",
            "y",
            "starting_enemies_number",
            "difficulty",
            "enemies",
            "enemy_leader",
        )


class UnlockLevelsSerializer(serializers.ModelSerializer):
    """
    PATCH запрос и пришел finished_level - значит мы открываем уровни, не пришел - тестовый запрос на обнуление
    """
    related_levels = serializers.ListField()
    finished_level = serializers.IntegerField()

    class Meta:
        model = UserLevel
        fields = ("id", "related_levels", "finished_level")

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        related_levels = validated_data.pop("related_levels", [])
        finished_level = validated_data.pop("finished_level", None)

        # если finished_level пришло, значит мы открываем юзеру все related_levels
        if finished_level:
            for level_id in related_levels:
                UserLevel.objects.get_or_create(user=user, level_id=level_id)
            instance.finished = True  # открыли все уровни и проставили что этот уровень завершён
            instance.save()
            levels = get_opened_user_levels(self=self, user_id=user.id, level_serializer=LevelSerializer)
            return {"levels": levels}

        # а здесь просто удалили все открытые уровни, кроме самого первого, а ему поставили что он не пройден
        UserLevel.objects.filter(user=user).exclude(level_id=1).delete()
        instance.finished = False
        instance.save()
        return {"deleted": 204}

    def to_representation(self, instance):
        # print(instance, 'из to-repr')
        return instance
