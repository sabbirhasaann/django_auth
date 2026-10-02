from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        })


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
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            return Response({
                'details': 'Invalid credentials',
            },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        access_token = AccessToken.for_user(user)
        return Response({
            "access": str(access_token),
        },
            status=status.HTTP_200_OK,
        )
