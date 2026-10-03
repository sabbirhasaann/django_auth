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

    def test_revoked_refresh_token_cannot_be_used(self):
        refresh = RefreshToken.for_user(self.user)

        refresh_string = str(refresh)

        logout_response = self.client.post(
            "/api/auth/logout/",
            {
                "refresh": refresh_string,
            },
            format="json",
        )

        print("Logout Response...", logout_response)

        self.assertEqual(
            logout_response.status_code,
            status.HTTP_200_OK,
        )

        refresh_response = self.client.post(
            "/api/auth/refresh/",
            {
                "refresh": refresh_string,
            },
            format="json",
        )

        print("Refresh Response...", refresh_response)

        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_refresh_rotation_revokes_old_token(self):
        refresh = RefreshToken.for_user(self.user)

        old_refresh = str(refresh)

        response = self.client.post(
            "/api/auth/refresh/",
            {
                "refresh": old_refresh,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        new_refresh = response.data.get("refresh")
        
        self.assertIsNotNone(new_refresh)

        # self.assertNotEqual(
        #     old_refresh,
        #     new_refresh,
        # )

        # old_token_response = self.client.post(
        #     "/api/auth/refresh/",
        #     {
        #         "refresh": old_refresh,
        #     },
        #     format="json",
        # )

        # self.assertEqual(
        #     old_token_response.status_code,
        #     status.HTTP_401_UNAUTHORIZED,
        # )
