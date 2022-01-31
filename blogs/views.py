from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blogs.models import Blog
from blogs.serializers import BlogSerializer
from utils.Extra import paginate, is_admin, is_owner


class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def get_queryset(self):
        return self.queryset.all().order_by('updated_at')

    def list(self, request, *args, **kwargs):
        return paginate(self)

    def create(self, request, *args, **kwargs):
        post_data = request.data.dict()
        serialize = self.get_serializer(data=post_data)
        serialize.is_valid(raise_exception=True)
        self.perform_create(serialize)
        return Response({'response': serialize.instance.title}, status=201)

    def update(self, request, *args, **kwargs):
        if not request.data:
            return Response({'error': 'No arguments found'})
        instance = self.get_object()
        post_data = request.data.dict()
        user = request.user_data
        if not is_admin(user):
            is_owner(user, instance)
        if post_data.get('authors') is not None:
            post_data['authors'] = post_data['authors'].split(', ')
        serialize = self.get_serializer(instance, data=post_data)
        serialize.is_valid(raise_exception=True)
        self.perform_update(serialize)
        return Response({'response': "ok"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user_data
        if not is_admin(user):
            is_owner(user, instance)
        self.perform_destroy(instance)
        return Response({'response': 'ok'})
