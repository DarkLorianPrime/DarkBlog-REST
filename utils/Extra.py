from rest_framework.authtoken.models import Token


def get_user(headers, return_user=True):
    token = headers.get('Authorization')
    user = Token.objects.filter(key=token.split(' ')[1])
    if return_user:
        return user.first().user
    return user
