from django.urls import include, path
from rest_framework import routers

from hits.views import HitViewSet

router = routers.DefaultRouter()
router.register(r"", HitViewSet, basename="hits")

urlpatterns = [
    path("", include(router.urls)),
]
