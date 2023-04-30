from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# create una funcion de crear usuairo paar reciclarala al momento de usar el test


def create_user(**params):
    """Create an return a user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = "http://localhost:8000/api"

    def test_register_user_success(self):
        """Test register an user in the plataform successful"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Jhon Doe",
        }

        response = self.client.post(f"{self.base_url}/signup/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload["email"])

        self.assertTrue(user.check_password(payload["password"]))

        self.assertNotIn("password", response.data)

    def test_register_user_with_email_exist(self):
        """Tests errror when register a user with an email previusly register"""
        payload = {
            "email": "john@example.com",
            "password": "testpass123",
            "name": "Jhon Doe",
        }

        create_user(**payload)
        response = self.client.post(f"{self.base_url}/signup/", payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short_error(self):
        payload = {
            "email": "john@example.com",
            "password": "ab",
            "name": "Jhon Doe",
        }

        response = self.client.post(
            f"{self.base_url}/signup/", payload=payload
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # confir that the user does not exist in databse
        user_exist = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )

        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Generate a token for a valid user credentials"""
        payload_register_user = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Jhon Doe",
        }

        create_user(**payload_register_user)

        payload = {
            "email": payload_register_user["email"],
            "password": payload_register_user["password"],
        }

        response = self.client.post(f"{self.base_url}/auth/login/", payload)

        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error_email_bad_credentials_at_create_token(self):
        """Tests return error if the credentials invalid"""
        create_user(email="test@example.com", password="goodpassword")

        payload = {"email": "", "password": "goodpassword"}

        response = self.client.post(f"{self.base_url}/auth/login/", payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

    def test_error_blank_password_at_create_token(self):
        """Tests return error if the credentials invalid"""
        create_user(email="test@example.com", password="goodpassword")

        payload = {"email": "test@example.com", "password": ""}

        response = self.client.post(f"{self.base_url}/auth/login/", payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)
