from datetime import datetime

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from blogs.models import Blog
from posts.models import Post, Comment
from posts.serializer import PostSerializer, CommentSerializer
from utils.Extra import paginate, is_admin
from utils.extra_editor import add_to_dict


class MainPage(ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(is_published=True, created_at__isnull=False).order_by("-created_at")[0:5].values()
        return Response({'response': queryset})


class Posts(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user_data
        post = Post.objects.filter(blog__id=self.kwargs['blog_id']).order_by('created_at')
        if not is_admin(user):
            if not Blog.objects.filter(id=self.kwargs['blog_id']).filter(Q(owner=user.id) | Q(authors__in=[user.id])):
                return post.filter(is_published=True)
        return post

    def list(self, request, *args, **kwargs):
        return paginate(self)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user_data
        instance.views.add(user)
        serializer = self.get_serializer(instance)
        return Response({'response': serializer.data})

    def update(self, request, *args, **kwargs):
        user = request.user_data
        if not is_admin(user):
            self.is_author(user)
        post_data = add_to_dict(request.POST.dict(), author=user.id, blog=self.kwargs['blog_id'], created_at=None)
        if post_data.get('is_published'):
            post_data['created_at'] = datetime.now()
        instance = self.get_object()
        serialize = self.get_serializer(instance, data=post_data)
        serialize.is_valid(raise_exception=True)
        self.perform_update(serialize)
        return Response({'response': serialize.instance.title})

    def create(self, request, *args, **kwargs):
        user = request.user_data
        if not is_admin(user):
            self.is_author(user)
        post_data = add_to_dict(request.POST.dict(), author=user.id, blog=self.kwargs['blog_id'], created_at=None)
        if post_data.get('is_published'):
            post_data['created_at'] = datetime.now()
        serialize = self.get_serializer(data=post_data)
        serialize.is_valid(raise_exception=True)
        self.perform_create(serialize)
        return Response({'response': serialize.instance.title})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user_data.id
        if not is_admin(user):
            self.is_author(user)
        Comment.objects.filter(post__id=instance.id).delete()
        self.perform_destroy(instance)
        return Response({'response': 'ok'})

    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user_data
        if instance.likes.filter(id=user.id).exists():
            instance.likes.remove(user)
            return Response({'response': 'ok'})
        instance.likes.add(user.id)
        return Response({'response': 'ok'})

    def is_author(self, user):
        blog = Blog.objects.filter(id=self.kwargs['blog_id']).filter(Q(authors__in=[user]) | Q(owner__id=user.id))
        if not blog.exists():
            raise ValidationError({'error': 'You are not owner or author.'})
        return True

    def havepermission(self, request, blog_id):
        user = request.user_data
        blog = Blog.objects.filter(id=blog_id).filter(Q(owner=user.id) | Q(authors__in=[user.id]))
        return Response({'response': blog.exists()})


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        post = Post.objects.filter(blog__id=self.kwargs['blog_id'], id=self.kwargs['post_id']).order_by('created_at')
        return Comment.objects.filter(post=post.first())

    def list(self, request, *args, **kwargs):
        return paginate(self)

    def create(self, request, *args, **kwargs):
        user = request.user_data
        post_data = add_to_dict(request.POST.dict(), author=user.id, post=self.kwargs['post_id'])
        serialize = self.get_serializer(data=post_data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response({'response': 'ok'})

    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_user(self.request.headers)
        if instance.like.filter(id=user.id).exists():
            instance.like.remove(user)
            return Response({'response': 'ok'})
        instance.like.add(user.id)
        return Response({'response': 'ok'})