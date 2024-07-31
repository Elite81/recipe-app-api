"""Tests fpr tje iser API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test crteateing a suer is successful."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_emai_exits_error(self):
        """Test error returned if user with email exist"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test Name",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_paassword_too_short_error(self):
        """test an error is returned if paasswrod less than 5 chars."""
        payload = {"email": "test@example.com",
                   "password": "test",
                   "name": "test Name"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""

        user_details = {
            "name": "test Name",
            "password": "test-user-password-123",
            "email": "test@example.com",
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
            # "name": user_details["name"],
        }
        res = self.client.post(TOKEN_URL, payload)
        # print(f'Hello: {res.data}')

        if "token" not in res.data:
            print(f"Error message: {res.data.get('error', 'No error message')}")
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_bad_credentials(self):
        """Test return error if credentials invalid."""
        create_user(name="test Name",
                    password="goodpass",
                    email="test@example.com")
        payload = {"email": "test@example.com",
                   "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_blank_passsword(self):
        """Test posting a blanck password return an error."""

        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrived_user_unauhorized(self):
        """Test authentication is requied for user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API request that require authentication."""

    def setUp(self):
        self.user = create_user(
            name="test Name",
            password="test-user-password123",
            email="test@example.com",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Tes retrieveing profile for logged in user."""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})

    def test_post_me_not_allowed(self):
        """Test POST is not allowed of the me endpoint."""
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile fo rthe authentiacted user."""
        payload = {"name": "Updated name", "password": "mewpasword123"}

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

