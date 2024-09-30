"""
Tests for Link APIs
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from shortener.models import Link

from link.serializers import LinkSerializer


LINKS_URL = reverse('link:link-list')

def create_link(user, **params):
    """Create a return a link"""
    link = Link.objects.create(
        user=user,
        original_url=params.get('original_url', 'https://example.com/test'),
        short_url=params.get('short_url', 'AAAbbb')
    )
    return link


class PublicLinkApiTests(TestCase):
    """Test unauthorized API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is requiered to call API"""
        res = self.client.get(LINKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateLinkApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_links(self):
        """Test retrieving a list of links"""
        create_link(self.user, original_url='https://example.com/test1', short_url='AAAbbb')
        create_link(self.user, original_url='https://example.com/test2', short_url='AAAccc')

        res = self.client.get(LINKS_URL)

        links = Link.objects.all().order_by('-id')
        serializer = LinkSerializer(links, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_link_list_limited_to_user(self):
        """Test lisf of links is limithed to authenticated user"""
        other_user = get_user_model().objects.create_user(
            'user2@example.com',
            'testpass123'
        )
        create_link(other_user, original_url='https://example.com/test1user2', short_url='AAAddd')
        create_link(other_user, original_url='https://example.com/test2user2', short_url='AAAccc')
        create_link(self.user)

        res = self.client.get(LINKS_URL)

        links = Link.objects.filter(user=self.user).order_by('-id')
        serializer = LinkSerializer(links, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)



        


