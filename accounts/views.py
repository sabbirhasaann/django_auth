from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    inline_serializer,
)
from rest_framework import serializers

from .models import User

from rest_framework import generics, viewsets

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

    @extend_schema(
        summary="Get user",
        description=(
            "Get user"
        ),
        request=None,
        responses={
            200: UserSerializer
        },
    )
    def get(self, request):
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )


class StatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Check authentication status",
        description=(
            "Returns whether the user is authenticated along with basic user"
            " details."
        ),
        responses={
            200: serializers.SerializerMetaclass(
                "StatusResponseSerializer",
                (serializers.Serializer,),
                {
                    "authenticated": serializers.BooleanField(
                        help_text="Indicates if the user is authenticated"
                    ),
                    "user_id": serializers.IntegerField(
                        help_text="The primary key of the user"
                    ),
                    "username": serializers.CharField(
                        help_text="The username of the user"
                    ),
                },
            )
        },
    )
    def get(self, request):
        print(request)
        return Response({
            'authenticated': True,
            'user_id': request.user.id,
            'username': request.user.username,
        })


class AccessTokenLoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get an access token by email and passowrd",
        description="Fetches access token",
        request=AccessTokenLoginSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access": {
                        "type": "string",
                        "example": "eyJhbGciOiJIUzI1Ni...",
                    }
                },
            }
        },
    )
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

    @extend_schema(
        summary="Refresh token",
        description=(
            "Takes a refresh token and returns a new access and refresh token"
            " pair."
        ),
        request=RefreshTokenSerializer,
        responses={
            200: serializers.SerializerMetaclass(
                "RefreshTokenResponseSerializer",
                (serializers.Serializer,),
                {
                    "access": serializers.CharField(
                        help_text="New JWT access token"
                    ),
                    "refresh": serializers.CharField(
                        help_text="New JWT refresh token"
                    ),
                },
            )
        },
    )
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

    @extend_schema(
        summary="Login api view",
        description="Login API",
        request=LoginSerializer,
        responses={
                200: inline_serializer(
                    name="Login Response",
                    fields={
                        "access": serializers.CharField(help_text="JWT access token"),
                        "refresh": serializers.CharField(help_text="JWT refresh token"),
                        "user": UserSerializer()
                    }
                )
        }
    )
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

    @extend_schema(
        summary="Logout endpoint",
        description=(
            "Server Side "
            "Logout"
        ),
        request=LogoutSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access": {
                        "type": "string",
                        'details': 'Successfully logged out.',
                    }
                },
            }
        }
    )
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

    @extend_schema(
        summary="Registration api endpoint",
        description="Submit registration infos..",
        request=RegisterSerializer,
        responses=UserSerializer

    )
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


class UsersListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        summary="Users list enpoint",
        description="Users list"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.PATH,
                description="The unique Id of the user"
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
