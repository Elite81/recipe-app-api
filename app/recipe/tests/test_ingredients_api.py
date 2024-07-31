'''Test for the ingrediants API'''
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from core.models import *

from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import IngredientSerializer


INGREDIANT_URL = reverse('recipe:ingredient-list')

def create_user(email='user@sample.com', password='testpass123'):
    '''Create and return user'''
    return get_user_model().objects.create_user(email=email, password=password)

class PublicIngerediantApiTest(TestCase):
    '''Test  unauthenticated API request'''

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        '''Test auth is requied for retrieving ingrediants'''
        res = self.client.get(INGREDIANT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngerediantApiTest(TestCase):
    '''Test authenticated API request'''

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)



    def test_retrieving_ingrediant(self):
        '''Test auth is requied for retrieving ingrediants'''
        Ingredient.objects.create(user=self.user, name='kite')
        Ingredient.objects.create(user=self.user, name='Vanilla')
        res = self.client.get(INGREDIANT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_ingrediant_limited_to_user(self):
        '''Test list of Ingrediants is limited to authenticated user.'''
        user2 = create_user(email='uer2@example.com')
        Ingredient.objects.create(user=user2, name='Salt')
        ingredient = Ingredient.objects.create(user=self.user, name='Peper')

        res = self.client.get(INGREDIANT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id )
