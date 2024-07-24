'''
Serializer for recipe APIs
'''
from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    '''Serializer for recipes.'''

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_onlly_field = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    '''Serializer for recipe detail view.'''

    class Meta(RecipeSerializer.Meta):
        '''Serializer for recipe detail view.'''
        fields = RecipeSerializer.Meta.fields + ['description']