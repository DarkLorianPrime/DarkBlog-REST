from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from authorizationserver.models import User, Roles, PostToken
from authorizationserver.serializer import LoginSerializer
from utils.decorators.login_decorators import is_not_logged_in, is_logged_in
from utils.decorators.token_decorators import is_not_token_valid


class Auth(ViewSet):
    @is_not_token_valid
    @is_not_logged_in
    def auth(self, request, *args, **kwargs):
        data = request.POST
        if data.get('username') is None and data.get('email') is None:
            raise ValidationError({'error': 'You didn`t specify your username or email.'})
        user = User.objects.filter(Q(username=data.get('username')) | Q(email=data.get('email')))
        if not user.exists():
            raise ValidationError({'error': 'This email or login is not found.'})
        if not user.first().check_password(data.get('password')):
            raise ValidationError({'error': 'Password incorrect.'})
        if request.role == 'Blocked':
            request.session['user'] = None
            return Response({'response': 'User blocked'})
        request.session['user'] = user.first().token
        return Response({'response': user.first().token})

    @is_not_logged_in
    @is_not_token_valid
    def registration(self, request, *args, **kwargs):
        serialize = LoginSerializer(data=request.POST)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        request.session['user'] = serialize.instance.token
        return Response({'response': 'ok'})

    @is_logged_in
    def logout(self, request, *args, **kwargs):
        request.session['user'] = None
        return Response({'response': 'exit'})

    def is_auth(self, request, *args, **kwargs):
        token = request.session.get('user')
        if token is None:
            return Response({'auth': 'NAuth'})
        profile = User.objects.filter(token=token)
        info = profile.values('first_name', 'last_name', 'username', 'email', 'avatar')
        return Response({'response': info, 'auth': 'Auth'})

    @is_logged_in
    def get_roles(self, request, *args, **kwargs):
        token = request.session.get('user')
        profile = User.objects.filter(token=token)
        roles = profile.first().role.all()
        return Response({'response': roles.values()})

    # @is_logged_in
    # def give_role(self, request, *args, **kwargs):
    #     token = request.session.get('user')
    #     profile = User.objects.filter(token=token)
    #     roles = profile.first().role.all()
    #     return Response({'response': roles.values()})


class TokenHandler(ViewSet):
    def get_token(self, request, *args, **kwargs):
        return Response({'response': PostToken.objects.filter().first().token})