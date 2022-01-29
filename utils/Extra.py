from functools import reduce

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


def get_user(headers, return_user=True):
    token = headers.get('Authorization')
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
