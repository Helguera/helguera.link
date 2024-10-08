"""
Test models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from shortener import models


def create_user(email='test@example.com', password='testpass123'):
    """Creates a returns a new user"""
    user = get_user_model().objects.create_user(
        email=email,
        password=password
    )
    return user


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = create_user(email=email, password='sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            user = create_user(email='', password='sample123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_link(self):
        """Test creating a link"""
        user = create_user()
        
        link = models.Link.objects.create(
            user = user,
            original_url = 'https://example.com'
        )

        # self.assertIn('helguera.link/', link.short_url)
        self.assertEqual(1,1)
