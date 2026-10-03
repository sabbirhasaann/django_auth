from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class TokenRevocationService:

    @staticmethod
    def revoke(refresh_token_string: str) -> None:

        try:
            refresh_token = RefreshToken(refresh_token_string)
            refresh_token.blacklist()

        except TokenError:
            raise
