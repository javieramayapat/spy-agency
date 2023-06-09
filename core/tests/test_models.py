""" Test for application model"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Hitman


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email without username succesfully"""
        email = "test@example.com"
        password = "testpass123"
        user = Hitman.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_hitman)

    def test_new_user_email_is_normalize(self):
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = Hitman.objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_a_user_without_an_email_raise_value_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpass123")

    def test_create_super_user(self):
        user = get_user_model().objects.create_superuser(
            "test@example.com", "test123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
