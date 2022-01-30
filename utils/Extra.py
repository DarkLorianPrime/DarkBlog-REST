from functools import reduce

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from authorizationserver.models import Roles
from blogs.models import Blog


def get_user(headers, return_user=True):
    token = headers.get('authorization')
    user = Token.objects.filter(key=token.split(' ')[1])
    if return_user:
        return user.first().user
    return user


def paginate(self, queryset=None):
    if queryset is None:
        queryset = self.get_queryset()
    if self.request.GET.get('limit') is None:
        raise ValidationError({'error': "You not pass 'limit'"})
    return reduce(lambda data, rec: rec(data), (queryset, self.paginate_queryset, lambda page: self.get_serializer(page, many=True).data, self.get_paginated_response))


def is_admin(user):
    role = user.role.filter(id=Roles.objects.filter(role="Admin").first().id)
    return True if role.exists() else False


def is_owner(user, instance):
    blog = Blog.objects.filter(owner__id=user.id).filter(id=instance.id)
    if not blog.exists():
        raise ValidationError({'error': 'You not owner.'})