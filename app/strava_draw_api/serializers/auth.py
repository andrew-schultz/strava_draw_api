from rest_framework import serializers
from .activity import ActivitySerializer

class AuthResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    activities = ActivitySerializer(many=True)


class AuthCodeRequestSerializer(serializers.Serializer):
    code = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    integration = serializers.BooleanField()


class SignUpSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()
