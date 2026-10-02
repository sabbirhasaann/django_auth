from rest_framework_simplejwt.tokens import RefreshToken


class TokenRevocationService:

    @staticmethod
    def revoke(refresh_token_string: str) -> None:
        refresh_token = RefreshToken(refresh_token_string)
        refresh_token.blacklist()
