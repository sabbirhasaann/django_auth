from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class AccessTokenLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        print(attrs)
        print(self)
        username = attrs['username']
        password = attrs['password']

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError("Invalid username and password")
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

    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={"input_type":"password"}
    )

    def validate(self, attrs):

        username = attrs["username"]
        password = attrs["password"]

        request = self.context.get("request")

        user = authenticate(
            request=request,
            username=username,
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
