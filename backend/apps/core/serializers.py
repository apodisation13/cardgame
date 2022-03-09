from rest_framework import serializers

from apps.core.models import Faction


class FactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faction
        fields = ("name", )
