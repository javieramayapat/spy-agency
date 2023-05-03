from rest_framework import serializers

from core.models import Hit, User


class HitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Hit
        fields = ["id", "target_name", "brief_description", "status"]


class HitDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Hit
        fields = [
            "id",
            "target_name",
            "brief_description",
            "status",
            "user",
            "assigned",
        ]


class HitStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        fields = ["status"]


class HitAssignedHitmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        fields = ["assigned"]

    def validate_assigned(self, value):
        if value.id == self.context["request"].user.id:
            raise serializers.ValidationError("No puedes asignarte a ti mismo")
        return value
