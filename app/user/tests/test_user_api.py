'''Tests fpr tje iser API'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    '''Create and return a new user.'''
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):


    def setUp(self):
        self.client  = APIClient()

    def test_create_user_success(self):
        '''Test crteateing a suer is successful.'''
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name':'test Name'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)


    def test_user_with_emai_exits_error(self):
        '''Test error returned if user with email exist'''
        payload = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'name':'test Name'}

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_paassword_too_short_error(self):
        '''test an error is returned if paasswrod less than 5 chars.'''
        payload = {
        'email': 'test@example.com',
        'password': 'test',
        'name':'test Name'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


