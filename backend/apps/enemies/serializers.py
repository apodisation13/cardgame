from rest_framework import serializers

from apps.core.serializers import EnemyLeaderAbilitySerializer, EnemyPassiveAbilitySerializer, MoveSerializer
from apps.enemies.models import Enemy, EnemyLeader, Level, UserLevel


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


class IdNameLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ("id", "name")


class LevelSerializer(serializers.ModelSerializer):
    enemies = EnemySerializer(many=True, read_only=True)
    enemy_leader = EnemyLeaderSerializer(many=False, read_only=True)
    # related_levels = IdNameLevelSerializer(many=True)

    class Meta:
        model = Level
        fields = (
            "id",
            "name",
            "starting_enemies_number",
            "difficulty",
            "enemies",
            "enemy_leader",
            "related_levels",
        )


class UserLevelsThroughSerializer(serializers.ModelSerializer):
    level = LevelSerializer(many=False)

    class Meta:
        model = UserLevel
        fields = ("level", "id")


class UnlockLevelsSerializer(serializers.ModelSerializer):
    """
    POST: юзер прошел уровень, ему ставим finished, открываем всех его детей - related_levels
    PATCH: тестовый запрос, удаление всех пройденных уровней, кроме первого
    """
    related_levels = serializers.ListField()
    finished_level = serializers.IntegerField()

    class Meta:
        model = UserLevel
        fields = ("id", "related_levels", "finished_level")

    # def create(self, validated_data):
    #     user = self.context.get('request').user
    #     to_be_unlocked, to_set_finished = validated_data["related_levels"], validated_data["finished_level"]
    #     for level_id in to_be_unlocked:
    #         UserLevel.objects.get_or_create(user=user, level_id=level_id)
    #     UserLevel.objects.filter(user=user, level_id=to_set_finished).update(finished=True)
    #     return {"status": 201}

    def update(self, instance, validated_data):
        print(instance.id)  # запись UserLevel, которая пришла в запросе
        user = self.context.get('request').user
        related_levels = validated_data.pop("related_levels", None)
        finished_level = validated_data.pop("finished_level", None)
        if finished_level:
            for level_id in related_levels:
                UserLevel.objects.get_or_create(user=user, level_id=level_id)
            instance.finished = True
            instance.save()
            return {"opened": 201}

        UserLevel.objects.filter(user=user).exclude(level_id=1).delete()
        instance.finished = False
        instance.save()
        return {"deleted": 204}

    def to_representation(self, instance):
        print(instance, 'из to-repr')
        return instance
