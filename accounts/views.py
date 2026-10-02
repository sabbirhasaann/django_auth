from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccessTokenLoginSerializer


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
