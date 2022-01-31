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
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.filter(Q(username=validated_data.get('username')) | Q(email=validated_data.get('email')))
        if user.exists():
            raise ValidationError({'error': 'This email or login already exists'})
        new_user = User.objects.create_user(username=validated_data.get('username'), email=validated_data.get('email'),
                                            password=validated_data.get('password'))
        new_user.role.add(Roles.objects.filter(role='User'))
        return new_user
