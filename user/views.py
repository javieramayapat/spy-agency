from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import AuthLoginTokenSerializer, UserSerializer


@extend_schema(
    tags=["Auth"],
    description="Register Usser in the system",
)
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


@extend_schema(
    tags=["Auth"],
    description="Login",
)
class CreateLoginTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthLoginTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
