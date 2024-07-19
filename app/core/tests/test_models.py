'''Test for models.'''

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    '''Test modles'''

    def test_create_usser_with_email_successfu(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_mew_user_email_normalized(self):
        ''' Test email normalized fro new user'''
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@example.com', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)


    def test_new_user_without_email_reases_error(self):
        ''' Test that creating a user withoug an email aise a ValueError'''

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def tst_create_superuser(self):
        '''Test createing a superuser.'''
        user = get_user_model().objects.create_superuser(
            'test@example.come',
            'test123',
        )
        self.assetTrue(user.is_superuser)
        self.assertTrue(user.is_staff)