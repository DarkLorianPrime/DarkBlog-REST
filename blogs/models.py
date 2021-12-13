from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('authorizationserver.User', on_delete=models.CASCADE, related_name='blog_user')
    authors = models.ManyToManyField('authorizationserver.User', related_name='authors_users', null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey('authorizationserver.User', on_delete=models.CASCADE, related_name='post_user')
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=2000)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='post_blog')
    views = models.ManyToManyField('authorizationserver.User', related_name='views_posts')
    likes = models.ManyToManyField('authorizationserver.User', related_name='likes_posts')


class Comment(models.Model):
    author = models.ForeignKey('authorizationserver.User', on_delete=models.CASCADE, related_name='comment_user')
    text = models.TextField(max_length=200)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comment_post')
    like = models.ManyToManyField('authorizationserver.User', related_name='likes_comments')
