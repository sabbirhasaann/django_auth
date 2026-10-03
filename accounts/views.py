from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    AccessTokenLoginSerializer,
    RefreshTokenSerializer,
    LoginSerializer,
    UserSerializer,
    LogoutSerializer,
    LoginResponseSerializer,
    RegisterSerializer,
)


from .services import (
    TokenRevocationService,
    TokenService,
)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            UserSerializer(request.user).data,
        )


class StatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request)
        return Response({
            'authenticated': True,
            'user_id': request.user.id,
            'username': request.user.username,
        })


class AccessTokenLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = AccessTokenLoginSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        access_token = AccessToken.for_user(user)
        return Response({
            "access": str(access_token),
        },
            status=status.HTTP_200_OK,
        )


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        return Response({
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh'],
        },
            status=status.HTTP_200_OK,
        )


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # refresh = RefreshToken.for_user(user)
        # access = refresh.access_token
        tokens = TokenService.create_token_pair(user)

        return Response({
            **tokens,
            "user": UserSerializer(user).data
        },

            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        TokenRevocationService.revoke(refresh_token)

        return Response({
            'details': 'Successfully logged out.'
        },
            status=status.HTTP_200_OK,
        )


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            "user": UserSerializer(user).data
        },
            status=status.HTTP_201_CREATED,
        )
