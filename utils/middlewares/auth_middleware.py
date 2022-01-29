import datetime
import uuid

from django.utils.deprecation import MiddlewareMixin

from authorizationserver.models import User, PostToken


class isAuth(MiddlewareMixin):
    def process_request(self, request):
        if request.session.get('auth_user') is None:
            request.users = None
            return
        user = User.objects.filter(token=request.session.get('auth_user')).first()
        if 'Blocked' in user.role.values_list('role', flat=True):
            request.session['user'] = None
            request.role = 'Blocked'
            return
        request.users = user
        request.role = user.role
        return


class CheckToken(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST':
            if request.POST.get('access_token') is None:
                request.token = 'Not passed'
                return
            token_object = PostToken.objects.filter(token=request.POST.get('access_token'))
            if not PostToken.objects.filter().exists():
                PostToken.objects.create(token=uuid.uuid4().hex)
                request.token = None
                return
            if not token_object.exists():
                request.token = None
                return
            if datetime.datetime.now() >= token_object.first().expires.replace(tzinfo=None):
                token_object.update(token=uuid.uuid4().hex,
                                    expires=datetime.datetime.now() + datetime.timedelta(minutes=30))
                request.token = 'Need update'
                return
            request.token = request.POST.get('access_token')
            return

