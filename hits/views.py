from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import authentication, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Hit
from core.permissions import IsBigBoss, IsHitman, IsManager, IsManagerOrBigBoss
from hits.serializers import (
    HitAssignedHitmanSerializer,
    HitDetailSerializer,
    HitSerializer,
    HitStatusSerializer,
)


class HitViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = HitSerializer
    queryset = Hit.objects.all()

    @permission_classes([IsHitman, IsManager, IsBigBoss])
    def list(self, request):
        user = request.user

        if user.is_hitman:
            queryset = Hit.objects.filter(Q(assigned=user.id)).order_by("-id")
        else:
            queryset = Hit.objects.all().order_by("-id")

        serializer = HitSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsManager, IsBigBoss])
    def retrieve(self, request, pk=None):
        hit = get_object_or_404(self.queryset, pk=pk)
        serializer = HitDetailSerializer(hit)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsManagerOrBigBoss])
    @extend_schema(request=HitSerializer, description="Create Hits")
    def create(self, request):
        serializer = HitSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.save(user_id=user.id)
            return Response(
                {"message": "Hit Created"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(request=HitSerializer, description="Update Hits")
    @permission_classes([IsAuthenticated, IsBigBoss])
    def update(self, request, pk=None):
        hit = Hit.objects.get(pk=pk)
        serializer = HitSerializer(hit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Hit Updated"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"])
    @extend_schema(
        request=HitStatusSerializer, description="Update Hits' status"
    )
    @permission_classes([IsAuthenticated, IsHitman, IsManager, IsBigBoss])
    def status(self, request, pk=None):
        hit = get_object_or_404(self.queryset, pk=pk)

        if hit.status in ["failed", "completed"]:
            raise ValidationError({"detail": "Cannot modify a closed Hit"})

        serializer = HitStatusSerializer(hit, data=request.data)
        if serializer.is_valid():
            hit.status = serializer.validated_data["status"]
            hit.save()
            return Response(
                {"message": "Hit status Updated"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @permission_classes([IsAuthenticated, IsBigBoss])
    @action(detail=True, methods=["post"])
    def assign_hitman(self, request, pk=None):
        hit = get_object_or_404(self.queryset, pk=pk)

        if hit.status in ["failed", "completed"]:
            raise ValidationError(
                {"detail": "Cannot assign a hitman to a closed hit"}
            )

        serializer = HitAssignedHitmanSerializer(
            hit, data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            hit.assigned = serializer.validated_data["assigned"]
            hit.save()
            return Response(
                {"message": "Hit Updated"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
