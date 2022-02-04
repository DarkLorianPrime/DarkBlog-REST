from django.db.models import Exists, OuterRef
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token

from authorizationserver.models import User


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.headers.get('authorization')
        if token is None:
            request.user_data = None
            return
        user = User.objects.filter(Exists(Token.objects.filter(key=token.split(' ')[1], user_id=OuterRef('id')))).first()
        request.user_data = user
        return
