from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class AccessTokenLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        print(attrs)
        print(self)
        email = attrs['email']
        password = attrs['password']

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("The account is inactive")

        attrs["user"] = user
        return attrs


class RefreshTokenSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = RefreshToken(attrs["refresh"])
        attrs["access"] = str(refresh_token.access_token)
        return attrs


class LoginSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )

    def validate(self, attrs):

        email = attrs["email"]
        password = attrs["password"]

        request = self.context.get("request")

        user = authenticate(
            request=request,
            email=email,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid username and password!"
            )
        if not user.is_active:
            raise serializers.ValidationError(
                "The account is inactive"
            )

        attrs["user"] = user
        return attrs


# class UserSerializer(serializers.Serializer):

#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(read_only=True)
#     email = serializers.EmailField(read_only=True)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "is_email_verified",
        ]

        read_only_fields = [
            "id",
            "is_email_verified",
        ]


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

class LoginResponseSerializer(serializers.Serializer):

    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()