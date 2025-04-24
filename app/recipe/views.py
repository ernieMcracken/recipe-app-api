"""Views for the recipe API"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipes"""

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    def get_queryset(self):
        """Retrieve recipes only for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        """Create a new recipe - set the user on the recipe to the current user"""
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """Manage Tags in the database"""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter tags to the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-name")
