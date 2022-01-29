import uuid

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from authorizationserver.models import User, Roles


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.filter(Q(username=validated_data.get('username')) | Q(email=validated_data.get('email')))
        if user.exists():
            raise ValidationError({'error': 'This email or login already exists'})
        new_user = User.objects.create_user(username=validated_data.get('username'), email=validated_data.get('email'), password=validated_data.get('password'))
        new_user.role.add(Roles.objects.filter(role='User'))
        return new_user

#     def validate(self, data):
#         if data.username is None and data.email is None:
#             raise ValidationError({'error': 'You didn`t specify your username or email'})
#         user = User.objects.filter(Q(username=data.username) | Q(email=data.email))
#         if not user.first().check_password(data.password):