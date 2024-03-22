from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_username(self, value):
        check_user_existence = User.objects.filter(username=value).exists()
        if check_user_existence:
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
