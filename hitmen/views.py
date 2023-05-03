from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import ManagerUser
from core.permissions import IsManagerOrBigBoss
from hitmen.serializers import (
    HitmenSerializer,
)


class HitmenViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManagerOrBigBoss]
    queryset = get_user_model().objects.all()
    serializer_class = HitmenSerializer

    def list(self, request):
        user = request.user

        if request.user.id == 1:
            queryset = get_user_model().objects.all().order_by("-id")
        else:
            manager_users = ManagerUser.objects.filter(manager=user)
            users = [manager_user.user for manager_user in manager_users]
            queryset = (
                get_user_model()
                .objects.filter(id__in=[user.id for user in users])
                .order_by("-id")
            )

        serializer = HitmenSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)

        if user.id == 1:
            return Response(
                {"error": "User cannot be deactivated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_active:
            user.is_active = False
            user.save()

            return Response(
                {"message": "Hitman Deactivate."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "error": "A deactivated hitman cannot be reactivated in the system."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    @method_decorator(permission_required("core.IsBigBoss"))
    def assign_manager(self, request, pk=None):
        """
        Permite que solo big boss pueda añadirle hitman a un manager
        """
        hitman = get_object_or_404(self.queryset, pk=pk, is_hitman=True)
        manager = get_object_or_404(
            self.queryset, pk=request.data.get("user_id")
        )

        # serializer = AssignHitmanToManagerSerializer(hitman, data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        manager_user = ManagerUser.objects.create(manager=manager, user=hitman)
        manager_user.save()

        return Response({"message": "Hitman assigned to Manager successfully"})
