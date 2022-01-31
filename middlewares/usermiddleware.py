from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.headers.get('authorization')
        user = Token.objects.filter(key=token.split(' ')[1]).first()
        request.user_data = user.user
        return
