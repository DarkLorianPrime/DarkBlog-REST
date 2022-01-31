from django.db.models import Exists
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token

from authorizationserver.models import User


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.headers.get('authorization')
        user = User.objects.filter(Exists(Token.objects.filter(key=token.split(' ')[1]))).first()
        request.user_data = user
        return
