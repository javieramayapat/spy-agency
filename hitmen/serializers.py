from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import ManagerUser, User


class HitmenSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "name", "is_active", "is_hitman", "is_manager"]


class AssignHitmanToManagerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    hitman = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_hitman=True)
    )

    def validate_user_id(self, value):
        try:
            manager = User.objects.get(pk=value, is_manager=True)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid user_id, not a manager."
            )
        return value

    def validate_hitman(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                "Cannot assign an inactive hitman."
            )
        if value.is_manager:
            raise serializers.ValidationError(
                "Cannot assign a hitman that is also a manager."
            )
        return value

    def create(self, validated_data):
        manager = User.objects.get(pk=validated_data["user_id"])
        hitman = validated_data["hitman"]
        manager_user, created = ManagerUser.objects.get_or_create(
            manager=manager, hitman=hitman
        )
        return manager_user
