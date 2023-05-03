from django.urls import include, path
from rest_framework import routers

from hitmen.views import HitmenViewSet

router = routers.DefaultRouter()
router.register(r"", HitmenViewSet, basename="hitmen")

urlpatterns = [
    path("", include(router.urls)),
]
