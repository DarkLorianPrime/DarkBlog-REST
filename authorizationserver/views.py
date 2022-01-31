from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authorizationserver.models import User
from authorizationserver.serializers import LoginSerializer, RegisterSerializer, UserSerializer


class PermissionAuth(ViewSet):
    def is_auth(self, request, *args, **kwargs):
        user = request.user_data
        if user is None:
            return Response({'auth': False})
        user = UserSerializer(user)
        return Response({'response': user.data, 'auth': True})

    def get_roles(self, request, *args, **kwargs):
        # Получает список ролей пользователя - готово
        user = request.user_data
        if user is None:
            return Response({'error': 'Not authentication'})
        roles = user.role.all()
        return Response({'response': roles.values()})


class Auth(ViewSet):
    permission_classes = []

    def auth(self, request, *args, **kwargs):
        data = request.POST

        serialize = LoginSerializer(data=data)
        serialize.is_valid(raise_exception=True)
        user = User.objects.filter(username=data.get('username'))
        if not user.exists():
            raise ValidationError({'error': 'This login is not found.'})
        if not user.first().check_password(data.get('password')):
            raise ValidationError({'error': 'Password incorrect.'})
        token = Token.objects.filter(user=user.first()).first().key
        return Response({'response': token})

    def registration(self, request, *args, **kwargs):
        serialize = RegisterSerializer(data=request.POST)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        token = Token.objects.create(user=serialize.instance)
        return Response({'reponse': token.key})
