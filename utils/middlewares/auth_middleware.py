from django.utils.deprecation import MiddlewareMixin

from authorizationserver.models import User


class isAuth(MiddlewareMixin):
    def process_request(self, request):
        if request.session.get('auth_user') is None:
            request.user = None
            return
        user = User.objects.filter(token=request.session.get('auth_user')).first()
        if user.role == 'Blocked':
            request.user = 'Blocked'

        request.user = user
        return
