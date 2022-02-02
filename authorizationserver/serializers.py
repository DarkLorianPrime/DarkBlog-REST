from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from authorizationserver.models import User, Roles


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'id', 'avatar']


class LoginSerializer(Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.filter(username=validated_data.get('username'))
        if user.exists():
            raise ValidationError({'error': 'This login already exists'})
        new_user = User.objects.create_user(**validated_data)
        new_user.role.add(Roles.objects.filter(role='User').first())
        return new_user
