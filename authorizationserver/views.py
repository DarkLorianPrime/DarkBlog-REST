from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from authorizationserver.models import User, Roles
from authorizationserver.serializer import LoginSerializer


class Login(ViewSet):
    def Auth(self, request, *args, **kwargs):
        data = request.POST
        if data.get('username') is None and data.get('email') is None:
            raise ValidationError({'error': 'You didn`t specify your username or email.'})
        user = User.objects.filter(Q(username=data.get('username')) | Q(email=data.get('email')))
        if not user.exists():
            raise ValidationError({'error': 'This email or login is not found.'})
        if not user.first().check_password(data.get('password')):
            raise ValidationError({'error': 'Password incorrect.'})
        request.session['user'] = user.first().token
        return Response({'response': user.first().token})

    def Registration(self, request, *args, **kwargs):
        serialize = LoginSerializer(data=request.POST)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        request.session['user'] = serialize.instance.token
        return Response({'response': 'ok'})

    def is_auth(self, request, *args, **kwargs):
        token = request.session.get('user')
        if token is None:
            return Response({'auth': 'NAuth'})
        profile = User.objects.filter(token=token).first()
        info = dict(profile.values())
        info['auth'] = 'Auth'
        return info
