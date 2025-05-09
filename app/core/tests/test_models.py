"""Tests for models"""

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

from unittest.mock import patch


def create_user(email="user@example.com", password="password123"):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        email = "test@example.com"
        password = "password123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email, password="password123"
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_value_error(self):
        """Test value error raised if email is not supplied"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "password1223")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            "test@example.com", "password123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successfull"""
        user = get_user_model().objects.create_user(
            email="test@example.com", password="password"
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is succesfull"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name="Tag 1")

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successfull"""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user, name="Ingredient 1"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch("core.models.uuid.uuid4")
    def test_recipe_file_uuid(self, mock_uuid):
        """Test generating image path"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")
