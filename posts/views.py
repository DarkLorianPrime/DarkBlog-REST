from datetime import datetime

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blogs.models import Blog
from posts.models import Post, Comment
from posts.serializer import PostSerializer
from utils.Extra import get_user
from utils.decorators.token_decorators import is_not_token_valid
from utils.extra_editor import add_to_dict


class Posts(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = get_user(self.request.headers)
        post = Post.objects.filter(blog__id=self.kwargs['blog_id']).order_by('created_at')
        if not Blog.objects.filter(id=self.kwargs['blog_id']).filter(Q(owner=user.id) | Q(authors__in=[user.id])):
            return post.filter(is_published=True)
        return post

    def list(self, request, *args, **kwargs):
        offset = self.request.GET.get('offset')
        queryset = self.get_queryset()
        if offset is None:
            return Response({'response': queryset.values()})
        if offset.isdigit():
            queryset = queryset.filter(id__gte=int(offset), id__lte=int(offset) + 20).values()
            return Response({'response': queryset})
        return ValidationError({'error': 'Offset has a error'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_user(self.request.headers)
        instance.views.add(user)
        serializer = self.get_serializer(instance)
        return Response({'response': serializer.data})

    def update(self, request, *args, **kwargs):
        user = get_user(self.request.headers)
        self.is_author(user)
        post_data = add_to_dict(request.POST.dict(), author=user.id, blog=self.kwargs['blog_id'], created_at=None)
        if post_data.get('is_published'):
            post_data['created_at'] = datetime.now()
        instance = self.get_object()
        serialize = self.get_serializer(instance, data=post_data)
        serialize.is_valid(raise_exception=True)
        self.perform_update(serialize)
        return Response({'response': serialize.instance.title})

    @is_not_token_valid
    def create(self, request, *args, **kwargs):
        user = get_user(self.request.headers)
        self.is_author(user)
        post_data = add_to_dict(request.POST.dict(), author=user.id, blog=self.kwargs['blog_id'], created_at=None)
        if post_data.get('is_published') is True:
            post_data['created_at'] = datetime.now()
        serialize = self.get_serializer(data=post_data)
        serialize.is_valid(raise_exception=True)
        self.perform_create(serialize)
        return Response({'response': serialize.instance.title})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_user(self.request.headers).id
        blog = Post.objects.filter(author__id=user).filter(id=instance.id)
        if not blog.exists():
            raise ValidationError({'error': 'You not owner.'})
        Comment.objects.filter(post__id=instance.id).delete()
        self.perform_destroy(instance)
        return Response({'response': 'ok'})

    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_user(self.request.headers)
        if instance.likes.filter(id=user.id).exists():
            instance.likes.remove(user)
            return Response({'response': 'ok'})
        instance.likes.add(user.id)
        return Response({'response': 'ok'})

    def havepermission(self, request, blog_id):
        user = get_user(self.request.headers)
        blog = Blog.objects.filter(id=blog_id).filter(Q(owner=user.id) | Q(authors__in=[user.id]))
        return Response({'response': blog.exists()})

    def is_author(self, user):
        blog = Blog.objects.filter(id=self.kwargs['blog_id']).filter(Q(authors__in=[user]) | Q(owner__id=user.id))
        if not blog.exists():
            raise ValidationError({'error': 'You are not owner or author.'})