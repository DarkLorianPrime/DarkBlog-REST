from functools import reduce

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authorizationserver.models import User, Roles
from blogs.models import Blog
from blogs.serializer import BlogSerializer
from utils.Extra import get_user, paginate, is_admin, is_owner
from utils.decorators.token_decorators import is_not_token_valid


class Blogs(ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def get_queryset(self):
        return self.queryset.all().order_by('updated_at')

    def list(self, request, *args, **kwargs):
        return paginate(self)

    @is_not_token_valid
    def create(self, request, *args, **kwargs):
        post_data = request.POST.dict()
        user = get_user(self.request.headers)
        post_data['owner'] = user.id
        serialize = self.serializer_class(data=post_data)
        serialize.is_valid(raise_exception=True)
        self.perform_create(serialize)
        return Response({'response': serialize.instance.title})

    def update(self, request, *args, **kwargs):
        if not request.data:
            return Response({'error': 'No arguments found'})
        instance = self.get_object()
        post_data = request.data.dict()
        user = get_user(self.request.headers)
        if not is_admin(user):
            is_owner(user, instance)
        post_data['owner'] = user.id
        if post_data.get('authors') is not None:
            post_data['authors'] = post_data['authors'].split(', ')
        serialize = self.get_serializer(instance, data=post_data)
        serialize.is_valid(raise_exception=True)
        self.perform_update(serialize)
        return Response({'response': "ok"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_user(self.request.headers)
        if not is_admin(user):
            is_owner(user, instance)
        self.perform_destroy(instance)
        return Response({'response': 'ok'})
