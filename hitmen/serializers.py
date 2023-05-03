from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from core.models import ManagerUser, User


class HitmenSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "name", "is_active", "is_hitman", "is_manager"]


class AssignHitmanToManagerSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def validate_manager_id(self, value):
        manager = get_object_or_404(User, pk=value)
        if not manager.is_manager:
            raise serializers.ValidationError(
                detail="Selected user is not a manager"
            )
        return value

    def validate(self, data):
        hitman_id = self.context.get("hitman_id")
        hitman = get_object_or_404(User, pk=hitman_id)
        if hitman.id == 1:
            raise serializers.ValidationError(
                detail="Manager assignment not allowed"
            )
        if not hitman.is_hitman:
            raise serializers.ValidationError(
                detail="Only hitmen can have managers"
            )
        if not hitman.is_active:
            raise serializers.ValidationError(
                detail="Cannot Assign a manager to inactive hitman"
            )
        return data

    def create(self, validated_data):
        manager_id = validated_data["manager_id"]
        hitman_id = self.context.get("hitman_id")
        manager = get_object_or_404(get_user_model(), pk=manager_id)
        hitman = get_object_or_404(get_user_model(), pk=hitman_id)
        manager_user = ManagerUser.objects.create(manager=manager, user=hitman)
        return manager_user
