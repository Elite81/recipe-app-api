"""Test for models."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from core import models


def create_user(email='use4r@example.com', password='testpass123'):
    '''Create and return a new user'''
    return get_user_model().objects.create_user(email=email, password=password)

class ModelTests(TestCase):
    """Test modles"""

    def test_create_usser_with_email_successful(self):
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email normalized fro new user"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@example.com", "Test2@example.com"],
            ["TEST3@example.com", "TEST3@example.com"],
            ["test4@example.com", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_reases_error(self):
        """Test that creating a user without an email raise a ValueError"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test createing a superuser."""
        user = get_user_model().objects.create_superuser(
            "test@example.come",
            "test123",
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_recipe(self):
        '''Test creating a recipe is successful'''
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title = 'Sample recipe name',
            time_minutes=5,
            price = Decimal('5.50'),
            description = 'Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)


    def test_create_tag(self):
        '''Test creating a tag is successful'''
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')
        self.assertEqual(str(tag), tag.name)


    def test_create_ingrediant(self):
        '''Test creating an ingerediant is successful.'''
        user = create_user()
        ingrediant = models.Ingredient.objects.create(
            user=user,
            name='Ingrediant'
        )

        self.assertEqual(str(ingrediant), ingrediant.name)



