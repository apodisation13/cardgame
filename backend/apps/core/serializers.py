from rest_framework import serializers

from apps.core.models import Ability, EnemyLeaderAbility, EnemyPassiveAbility, Faction, Move, PassiveAbility


class FactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faction
        fields = ("name", )


class AbilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Ability
        fields = ("name", "description")


class PassiveAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PassiveAbility
        fields = ("name", "description")


class MoveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Move
        fields = ("name", "description")


class EnemyPassiveAbilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = EnemyPassiveAbility
        fields = ("name", "description")


class EnemyLeaderAbilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = EnemyLeaderAbility
        fields = ("name", "description")
