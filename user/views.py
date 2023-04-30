from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import AuthLoginTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CreateLoginTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthLoginTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
