'''Test for recipe APIs'''

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from django.contrib.auth import get_user_model
from recipe.serializers import (RecipeSerializer, RecipeDetailSerializer)

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    '''Create and return a recipe detail URL'''
    return reverse('revipe: recpe-detail', args=[recipe_id])

def create_recipe(user, **params):
    '''Create and return a sample recipe'''
    default = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http.example.com/recipe.pdf'
    }
    default.update(params)
    recipe = Recipe.objects.create(user=user, **default)
    return recipe


class PiblicRecipeAPITest(TestCase):
    '''Test unauthenticated API request.'''

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        '''Test auth is required to call API'''
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    '''Test athenticated API requests.'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipe(self):
        '''Test retieving a list recipes'''
        create_recipe(user=self.user)
        # create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


def test_recipe_list_limited_to_user(self):
    '''Test lis of recipes is limited to authenticated user.'''
    other_user = get_user_model().objects.create_user(
        'example@gmail.com',
        'password123'
    )
    create_recipe(user=other_user)
    create_recipe(user=self.user)

    res = self.client.get(RECIPES_URL)

    recipes = Recipe.objects.filter(user=self.user)
    serializer =RecipeSerializer(recipes, many=True)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)




def test_get_recipe_detail(self):
    '''Test get recipe details.'''
    recipe = create_recipe(user=self.user)
    url = detail_url(recipe.id)
    res = self.client.get(url)
    serializer = RecipeDetailSerializer(recipe)
    self.assetEqula(res.data, serializer.data)


def test_create_recipe(self):
    '''Test creating a recipe'''
    payload = {
        'title': 'Sample recipe',
        'tiem_minute': 30,
        'price': Decimal('5.90')
    }
    res = self.client.post(RECIPES_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    recipe = Recipe.objects.get(id=res.data['id'])
    for k, v in payload.items():
        self.assertEqual(getattr(recipe, k), v)
    self.assertEqual(recipe.user, self.user)