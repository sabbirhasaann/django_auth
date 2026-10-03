from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TokenRevocationTests(APITestCase):
    """Token Revocation Test"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_refresh_token_can_be_revoked(self):
        """Test 1"""
        refresh = RefreshToken.for_user(self.user)

        response = self.client.post(
            "/api/auth/logout/",
            {
                "refresh": str(refresh)
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)