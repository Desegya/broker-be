from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import UserProfile
from unittest.mock import patch


class AuthBalanceAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.profile = UserProfile.objects.create(user=self.user, balance=100)
        self.client = APIClient()

    @patch("accounts.models.requests.get")
    def test_jwt_token_and_balance(self, mock_get):
        # Mock exchangerate.host API response
        mock_get.return_value.json.return_value = {"rates": {"EUR": 2.0}}
        # Obtain JWT token
        response = self.client.post(
            "/api/token/", {"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.json()["access"]

        # Access balance endpoint with token
        response = self.client.get(
            "/api/balance/?currency=EUR", HTTP_AUTHORIZATION=f"Bearer {access}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("balance", data)
        self.assertIn("balance_converted", data)
        self.assertEqual(data["balance_converted"], 200.00)

    def test_balance_requires_auth(self):
        response = self.client.get("/api/balance/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
