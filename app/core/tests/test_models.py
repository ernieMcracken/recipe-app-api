"""Tests for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        email = "test@example.com"
        password = "password123"
        user = get_user_model().objects.create_user(email=email, password=password)

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
