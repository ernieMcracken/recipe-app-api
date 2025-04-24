"""Tests for the tags API"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")


def create_user(email="user@exmaple.com", password="password123"):
    """Create and return a user"""
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(tag_id):
    """Return tag detail url"""
    return reverse("recipe:tag-detail", args=[tag_id])


class PublicAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags"""
        Tag.objects.create(user=self.user, name="Breakfast")
        Tag.objects.create(user=self.user, name="Dinner")
        Tag.objects.create(user=self.user, name="Tea")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")

        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test tags list is limited to authenticated user"""
        user2 = create_user(email="user2@example.com")

        tag = Tag.objects.create(user=self.user, name="Dinner")
        Tag.objects.create(user=user2, name="Tea")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)

    def test_update_tag(self):
        """Test updating a tag"""
        tag = Tag.objects.create(user=self.user, name="Dinner")

        payload = {"name": "Tea"}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_tag = Tag.objects.get(pk=tag.id)
        self.assertEqual(updated_tag.name, payload["name"])

    def test_delete_tag(self):
        """Test deleting a tag"""
        tag = Tag.objects.create(name="Test tag", user=self.user)
        url = detail_url(tag.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())
