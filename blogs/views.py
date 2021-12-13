from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authorizationserver.models import User
from blogs.models import Blog
from blogs.serializer import BlogSerializer
from utils.decorators.login_decorators import is_logged_in
from utils.decorators.token_decorators import is_not_token_valid


class MyBlogs(ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def get_queryset(self):
        user = User.objects.filter(token=self.request.session.get('user'))
        return self.queryset.filter(user=user.first().id)


class Blogs(ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def get_queryset(self):
        user = User.objects.filter(token=self.request.session.get('user'))
        if not user.exists():
            raise ValidationError({'error': 'You not logged in.'})
        return self.queryset.all().order_by('created_at')

    @is_not_token_valid
    @is_logged_in
    def create(self, request, *args, **kwargs):
        post_data = request.POST.dict()
        user = User.objects.filter(token=self.request.session.get('user'))
        post_data['owner'] = user.first().id
        serialize = self.serializer_class(data=post_data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response({'response': serialize.instance.title})

    @is_logged_in
    def list(self, request, *args, **kwargs):
        offset = self.request.GET.get('offset')
        queryset = self.get_queryset()
        if offset is None:
            raise ValidationError({'error': 'Offset can`t be empty'})
        if offset.isdigit():
            queryset = queryset.filter(id__gte=int(offset), id__lte=int(offset) + 20).values()
            return Response({'response': queryset})
        return Response({'response': queryset.values()})