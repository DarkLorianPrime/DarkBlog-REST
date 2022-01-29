from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authorizationserver.models import User, PostToken
from authorizationserver.serializer import LoginSerializer
from utils.decorators.token_decorators import is_not_token_valid


class Permission_Auth(ViewSet):
    def is_auth(self, request, *args, **kwargs):
        # авторизован ли пользователь? - готово
        token = request.headers.get('Authorization')
        if token is None:
            return Response({'auth': False})
        profile = Token.objects.filter(key=token.split(' ')[1]).first()
        profile_info = User.objects.filter(id=profile.user.id).values('username', 'first_name', 'last_name', 'email',
                                                                      'id', 'avatar', )
        return Response({'response': profile_info, 'auth': True})

    def get_roles(self, request, *args, **kwargs):
        # Получает список ролей пользователя - готово
        token = request.headers.get('Authorization')
        profile = Token.objects.filter(key=token.split(' ')[1]).first().user
        roles = profile.role.all()
        return Response({'response': roles.values()})


class Auth(ViewSet):
    permission_classes = []

    @is_not_token_valid
    def auth(self, request, *args, **kwargs):
        # авторизация - готово
        data = request.POST
        if data.get('username') is None and data.get('email') is None:
            raise ValidationError({'error': 'You didn`t specify your username or email.'})
        user = User.objects.filter(Q(username=data.get('username')) | Q(email=data.get('email')))
        if not user.exists():
            raise ValidationError({'error': 'This email or login is not found.'})
        if not user.first().check_password(data.get('password')):
            raise ValidationError({'error': 'Password incorrect.'})
        token = Token.objects.filter(user=user.first()).first().key
        return Response({'response': token})

    @is_not_token_valid
    def registration(self, request, *args, **kwargs):
        # регистрация - готово
        serialize = LoginSerializer(data=request.POST)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        token = Token.objects.create(user=serialize.instance)
        return Response({'reponse': token.key})

    # @is_logged_in
    # def give_role(self, request, *args, **kwargs):
    #     token = request.session.get('user')
    #     profile = User.objects.filter(token=token)
    #     roles = profile.first().role.all()
    #     return Response({'response': roles.values()})


class TokenHandler(ViewSet):
    permission_classes = []

    def get_token(self, request, *args, **kwargs):
        return Response({'response': PostToken.objects.filter().first().token})
