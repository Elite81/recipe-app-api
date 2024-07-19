"""View for the user API"""

from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializer,
    AuthokentSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthokentSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
